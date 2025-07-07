from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from Compiler.forms import CodeSubmissionForm
from django.conf import settings
import time
import signal
import platform;
import os
import uuid
import subprocess
from pathlib import Path


def submit(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            print(submission.language)
            print(submission.code)
            output = run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data = output
            submission.save()

            template = loader.get_template("index.html")
            context = {"submission": submission}
            return HttpResponse(template.render(context, request))
    else:
        form = CodeSubmissionForm()
    
    template = loader.get_template("index.html")
    context = {"form": form}
    return HttpResponse(template.render(context, request))


def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())
    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass  # Just create the file

    runtime = None
    output_data = ""
    verdict = "Accepted"

    try:
        # --- C++ ---
        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(["g++", str(code_file_path), "-o", str(executable_path)])

            if compile_result.returncode != 0:
                verdict = "Compilation Error"
                return {"output": "Compilation Error", "runtime": "0s", "verdict": verdict}

            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                start = time.time()
                if platform.system() == "Windows":
                    process = subprocess.Popen(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                else:
                    process = subprocess.Popen(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        preexec_fn=os.setsid
                    )
                try:
                    process.wait(timeout=2)
                    runtime = time.time() - start
                except subprocess.TimeoutExpired:
                    if platform.system() == "Windows":
                        process.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    verdict = "Time Limit Exceeded"
                    return {"output": "", "runtime": ">2s", "verdict": verdict}

        # --- Python ---
        elif language == "py":
            with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
                start = time.time()
                if platform.system() == "Windows":
                    process = subprocess.Popen(
                        ["python", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                else:
                    process = subprocess.Popen(
                        ["python", str(code_file_path)],
                        stdin=input_file,
                        stdout=output_file,
                        stderr=subprocess.PIPE,
                        preexec_fn=os.setsid
                    )
                try:
                    process.wait(timeout=2)
                    runtime = time.time() - start
                except subprocess.TimeoutExpired:
                    if platform.system() == "Windows":
                        process.send_signal(signal.CTRL_BREAK_EVENT)
                    else:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    verdict = "Time Limit Exceeded"
                    return {"output": "", "runtime": ">2s", "verdict": verdict}

        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()

    except Exception as e:
        verdict = "Runtime Error"
        output_data = str(e)

    return {
        "output": output_data.strip(),
        "runtime": f"{runtime:.3f}s" if runtime else "0s",
        "verdict": verdict
    }
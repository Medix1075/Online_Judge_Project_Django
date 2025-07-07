from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Problem, TestCase
from .forms import ProblemForm
from django.contrib.auth.decorators import user_passes_test
from Compiler.forms import CodeSubmissionForm  # if using a form
from Compiler.models import CodeSubmission     # if using model directly
from Compiler.views import run_code
from .utils.gemini import generate_hint, analyze_code
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@csrf_exempt  # Optional, if CSRF isn't working via JS
@require_POST
def generate_ai_review(request, pk):
    body = json.loads(request.body)
    task = body.get("task")
    code = body.get("code", "")
    problem = get_object_or_404(Problem, pk=pk)

    if task == "hint":
        review = generate_hint(problem)
    elif task == "analysis":
        review = analyze_code(problem, code)
    else:
        return JsonResponse({"error": "Invalid task"}, status=400)

    return JsonResponse({'review': review})

def home_page(request):
    problems = Problem.objects.all()[:3]  # Optional filtering
    return render(request, 'home.html', {'problems': problems})

# List all problems
def problem_list(request):
    problems = Problem.objects.all()
    template = loader.get_template('problem_list.html')
    context = {'problems': problems}
    return HttpResponse(template.render(context, request))


# View a single problem
@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    sample_testcases = TestCase.objects.filter(problem=problem, is_sample=True)
    all_testcases = TestCase.objects.filter(problem=problem)  # includes hidden testcases

    if not problem.ai_review:
        review_response = generate_ai_review(request, pk)
        if isinstance(review_response, JsonResponse):
            problem.ai_review = json.loads(review_response.content).get("review")
            problem.save()
            
    submission = None
    verdict = None
    runtime = None
    passed_testcases = None
    failed_testcase_number = None

    show_output = False
    show_verdict = False
    test_case_results = []

    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        action = request.POST.get("action")

        if form.is_valid():
            submission = form.save(commit=False)
            submission.problem = problem
            
            
            if action == "run":
                result = run_code(submission.language, submission.code, submission.input_data)
                submission.output_data = result["output"]
                submission.verdict = result["verdict"]
                submission.runtime = result["runtime"]
                show_output = True

            elif action == "submit":
                show_verdict = True
                passed = 0
                has_failed_hidden = False

                for idx, testcase in enumerate(all_testcases, start=1):
                    test_result = run_code(submission.language, submission.code, testcase.input_data)
                    output = test_result["output"]
                    verdict = test_result["verdict"]

                    passed_this = (
                        output.strip() == testcase.expected_output.strip()
                        and verdict == "Accepted"
                    )

                    test_case_results.append({
                        'status': 'Passed' if passed_this else (verdict if verdict != "Accepted" else "Failed"),
                        'passed': passed_this,
                        'is_sample': testcase.is_sample,
                        'number': idx,
                    })

                    if not passed_this:
                        if not testcase.is_sample:
                            submission.verdict = verdict if verdict != "Accepted" else "Wrong Answer"
                            failed_testcase_number = f"Test case {idx} failed"
                            has_failed_hidden = True
                            break
                    else:
                        passed += 1

                if not has_failed_hidden:
                    submission.verdict = "Accepted"

                submission.output_data = output
                submission.runtime = test_result.get("runtime", None)

            submission.save()
            verdict = submission.verdict
            runtime = submission.runtime

    else:
        form = CodeSubmissionForm()

    context = {
        'problem': problem,
        'form': form,
        'sample_testcases': sample_testcases,
        'submission': submission,
        'verdict': verdict,
        'runtime': runtime,
        'passed_testcases': passed_testcases,
        'failed_testcase_number': failed_testcase_number,
        'show_output': show_output,
        'show_verdict': show_verdict,
        'test_case_results': test_case_results,
    }

    template = loader.get_template('problem_details.html')
    return HttpResponse(template.render(context, request))




# Admin (or staff) can add problems
@user_passes_test(lambda u: u.is_staff)
def problem_create(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('problem_list')
    else:
        form = ProblemForm()

    template = loader.get_template('problem_form.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))

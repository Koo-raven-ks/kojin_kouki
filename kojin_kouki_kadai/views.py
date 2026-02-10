from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from .models import Lecture, Assignment, SubmissionRecord, Grading
from .forms import LectureForm, AssignmentForm, SubmissionRecordForm, GradingForm


def index(request):
    """ダッシュボード - 課題一覧と統計情報を表示"""
    all_assignments = Assignment.objects.all().order_by("due_date")
    pending_assignments = all_assignments.filter(status="pending").order_by("due_date")
    submitted_assignments = all_assignments.filter(status="submitted")
    graded_assignments = all_assignments.filter(status="graded")

    # 優先度別にソート
    urgent = pending_assignments.filter(priority="high")

    # グラフ用データ：優先度別
    high_priority = all_assignments.filter(priority="high").count()
    medium_priority = all_assignments.filter(priority="medium").count()
    low_priority = all_assignments.filter(priority="low").count()

    # グラフ用データ：期限別（未提出のみ）
    today = timezone.now().date()
    overdue = pending_assignments.filter(due_date__lt=timezone.now()).count()
    this_week = pending_assignments.filter(
        due_date__gte=timezone.now(),
        due_date__lt=timezone.now() + timezone.timedelta(days=7),
    ).count()
    next_week = pending_assignments.filter(
        due_date__gte=timezone.now() + timezone.timedelta(days=7),
        due_date__lt=timezone.now() + timezone.timedelta(days=14),
    ).count()
    later = pending_assignments.filter(
        due_date__gte=timezone.now() + timezone.timedelta(days=14)
    ).count()

    # グラフ用データ：講義別
    from django.db.models import Count

    lectures_data = list(
        Lecture.objects.annotate(assignment_count=Count("assignments"))
        .values("name", "assignment_count")
        .order_by("-assignment_count")[:5]
    )

    context = {
        "all_assignments": all_assignments,
        "pending_count": pending_assignments.count(),
        "submitted_count": submitted_assignments.count(),
        "graded_count": graded_assignments.count(),
        "urgent_count": urgent.count(),
        "urgent_assignments": urgent[:5],
        # グラフデータ
        "high_priority": high_priority,
        "medium_priority": medium_priority,
        "low_priority": low_priority,
        "overdue": overdue,
        "this_week": this_week,
        "next_week": next_week,
        "later": later,
        "lectures_data": lectures_data,
    }
    return render(request, "kojin_kouki_kadai/index.html", context)


# ===== Lecture CRUD =====
class LectureListView(generic.ListView):
    """講義一覧"""

    model = Lecture
    template_name = "kojin_kouki_kadai/lecture_list.html"
    context_object_name = "lectures"
    ordering = ["day_of_week", "start_time"]


class LectureDetailView(generic.DetailView):
    """講義詳細 - 関連する課題も表示"""

    model = Lecture
    template_name = "kojin_kouki_kadai/lecture_detail.html"
    context_object_name = "lecture"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["assignments"] = self.object.assignments.all().order_by("due_date")
        return context


class LectureCreateView(generic.CreateView):
    """講義作成"""

    model = Lecture
    form_class = LectureForm
    template_name = "kojin_kouki_kadai/lecture_form.html"
    success_url = reverse_lazy("lecture_list")


class LectureUpdateView(generic.UpdateView):
    """講義編集"""

    model = Lecture
    form_class = LectureForm
    template_name = "kojin_kouki_kadai/lecture_form.html"
    success_url = reverse_lazy("lecture_list")


class LectureDeleteView(generic.DeleteView):
    """講義削除"""

    model = Lecture
    template_name = "kojin_kouki_kadai/lecture_confirm_delete.html"
    success_url = reverse_lazy("lecture_list")


# ===== Assignment CRUD =====
class AssignmentListView(generic.ListView):
    """課題一覧（フィルタリング機能付き）"""

    model = Assignment
    template_name = "kojin_kouki_kadai/assignment_list.html"
    context_object_name = "assignments"
    ordering = ["due_date"]
    paginate_by = 20

    def get_queryset(self):
        queryset = Assignment.objects.all().order_by("due_date")

        # ステータスフィルタ
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # 優先度フィルタ
        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        # 講義フィルタ
        lecture = self.request.GET.get("lecture")
        if lecture:
            queryset = queryset.filter(lecture__id=lecture)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lectures"] = Lecture.objects.all()
        context["status_choices"] = Assignment.STATUS_CHOICES
        context["priority_choices"] = Assignment.PRIORITY_CHOICES
        return context


class AssignmentDetailView(generic.DetailView):
    """課題詳細"""

    model = Assignment
    template_name = "kojin_kouki_kadai/assignment_detail.html"
    context_object_name = "assignment"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submission"] = (
            self.object.submission if hasattr(self.object, "submission") else None
        )
        return context


class AssignmentCreateView(generic.CreateView):
    """課題作成"""

    model = Assignment
    form_class = AssignmentForm
    template_name = "kojin_kouki_kadai/assignment_form.html"
    success_url = reverse_lazy("assignment_list")


class AssignmentUpdateView(generic.UpdateView):
    """課題編集"""

    model = Assignment
    form_class = AssignmentForm
    template_name = "kojin_kouki_kadai/assignment_form.html"
    success_url = reverse_lazy("assignment_list")


class AssignmentDeleteView(generic.DeleteView):
    """課題削除"""

    model = Assignment
    template_name = "kojin_kouki_kadai/assignment_confirm_delete.html"
    success_url = reverse_lazy("assignment_list")


# ===== SubmissionRecord CRUD =====
class SubmissionRecordCreateView(generic.CreateView):
    """提出記録作成（課題に紐付ける）"""

    model = SubmissionRecord
    form_class = SubmissionRecordForm
    template_name = "kojin_kouki_kadai/submission_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment_id = self.kwargs.get("assignment_id")
        context["assignment"] = get_object_or_404(Assignment, pk=assignment_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        assignment_id = self.kwargs.get("assignment_id")
        initial["assignment"] = get_object_or_404(Assignment, pk=assignment_id)
        initial["submitted_at"] = timezone.now()
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)
        # ステータスを「提出済み」に更新
        self.object.assignment.status = "submitted"
        self.object.assignment.save()
        return response

    def get_success_url(self):
        return reverse_lazy(
            "assignment_detail", kwargs={"pk": self.object.assignment.pk}
        )


class SubmissionRecordUpdateView(generic.UpdateView):
    """提出記録編集"""

    model = SubmissionRecord
    form_class = SubmissionRecordForm
    template_name = "kojin_kouki_kadai/submission_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "assignment_detail", kwargs={"pk": self.object.assignment.pk}
        )


class SubmissionRecordDeleteView(generic.DeleteView):
    """提出記録削除"""

    model = SubmissionRecord
    template_name = "kojin_kouki_kadai/submission_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "assignment_detail", kwargs={"pk": self.object.assignment.pk}
        )


# ===== Grading CRUD（先生用）=====
class GradingCreateView(generic.CreateView):
    """採点記録作成（先生用）"""

    model = Grading
    form_class = GradingForm
    template_name = "kojin_kouki_kadai/grading_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        submission_id = self.kwargs.get("submission_id")
        context["submission"] = get_object_or_404(SubmissionRecord, pk=submission_id)
        return context

    def form_valid(self, form):
        submission_id = self.kwargs.get("submission_id")
        form.instance.submission = get_object_or_404(SubmissionRecord, pk=submission_id)
        response = super().form_valid(form)
        # ステータスを「採点済み」に更新
        self.object.submission.assignment.status = "graded"
        self.object.submission.assignment.save()
        return response

    def get_success_url(self):
        return reverse_lazy(
            "assignment_detail", kwargs={"pk": self.object.submission.assignment.pk}
        )


class GradingUpdateView(generic.UpdateView):
    """採点記録編集（先生用）"""

    model = Grading
    form_class = GradingForm
    template_name = "kojin_kouki_kadai/grading_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submission"] = self.object.submission
        return context

    def get_success_url(self):
        return reverse_lazy(
            "assignment_detail", kwargs={"pk": self.object.submission.assignment.pk}
        )


class GradingDeleteView(generic.DeleteView):
    """採点記録削除（先生用）"""

    model = Grading
    template_name = "kojin_kouki_kadai/grading_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "assignment_detail", kwargs={"pk": self.object.submission.assignment.pk}
        )

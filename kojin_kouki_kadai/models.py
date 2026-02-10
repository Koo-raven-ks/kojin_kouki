from django.db import models
from django.utils import timezone


class Lecture(models.Model):
    """講義モデル"""

    name = models.CharField(max_length=100, verbose_name="講義名")
    instructor = models.CharField(max_length=100, verbose_name="講師名")
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ("Monday", "月"),
            ("Tuesday", "火"),
            ("Wednesday", "水"),
            ("Thursday", "木"),
            ("Friday", "金"),
            ("Saturday", "土"),
            ("Sunday", "日"),
        ],
        verbose_name="曜日",
    )
    start_time = models.TimeField(verbose_name="開始時刻")
    end_time = models.TimeField(verbose_name="終了時刻")
    classroom = models.CharField(max_length=100, verbose_name="教室")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "講義"
        verbose_name_plural = "講義"
        ordering = ["day_of_week", "start_time"]

    def __str__(self):
        return f"{self.name} ({self.day_of_week})"


class Assignment(models.Model):
    """課題モデル"""

    PRIORITY_CHOICES = [
        ("low", "低"),
        ("medium", "中"),
        ("high", "高"),
    ]

    STATUS_CHOICES = [
        ("pending", "未提出"),
        ("submitted", "提出済み"),
        ("graded", "採点済み"),
    ]

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="講義",
    )
    title = models.CharField(max_length=200, verbose_name="課題名")
    description = models.TextField(blank=True, verbose_name="説明")
    due_date = models.DateTimeField(verbose_name="提出期限")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium", verbose_name="優先度"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="ステータス",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name = "課題"
        verbose_name_plural = "課題"
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.title} ({self.lecture.name})"

    @property
    def is_overdue(self):
        """期限超過判定"""
        return timezone.now() > self.due_date and self.status == "pending"

    @property
    def days_until_due(self):
        """提出期限までの日数"""
        delta = self.due_date - timezone.now()
        return delta.days


class SubmissionRecord(models.Model):
    """提出記録モデル"""

    assignment = models.OneToOneField(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submission",
        verbose_name="課題",
    )
    submitted_at = models.DateTimeField(verbose_name="提出日時")
    notes = models.TextField(blank=True, verbose_name="備考")

    class Meta:
        verbose_name = "提出記録"
        verbose_name_plural = "提出記録"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.assignment.title} - 提出済み"


class Grading(models.Model):
    """採点記録モデル（先生のみが編集可能）"""

    submission = models.OneToOneField(
        SubmissionRecord,
        on_delete=models.CASCADE,
        related_name="grading",
        verbose_name="提出記録",
    )
    grade = models.IntegerField(verbose_name="成績")
    feedback = models.TextField(blank=True, verbose_name="フィードバック")
    graded_at = models.DateTimeField(auto_now=True, verbose_name="採点日時")

    class Meta:
        verbose_name = "採点記録"
        verbose_name_plural = "採点記録"
        ordering = ["-graded_at"]

    def __str__(self):
        return f"{self.submission.assignment.title} - {self.grade}点"

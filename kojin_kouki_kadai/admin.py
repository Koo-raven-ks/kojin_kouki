from django.contrib import admin
from .models import Lecture, Assignment, SubmissionRecord, Grading


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "day_of_week", "start_time", "classroom")
    list_filter = ("day_of_week", "created_at")
    search_fields = ("name", "instructor", "classroom")
    ordering = ("day_of_week", "start_time")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lecture",
        "due_date",
        "priority",
        "status",
        "days_until_due",
    )
    list_filter = ("status", "priority", "lecture", "due_date")
    search_fields = ("title", "lecture__name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("基本情報", {"fields": ("lecture", "title", "description")}),
        ("期限と優先度", {"fields": ("due_date", "priority")}),
        ("ステータス", {"fields": ("status",)}),
        (
            "タイムスタンプ",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(SubmissionRecord)
class SubmissionRecordAdmin(admin.ModelAdmin):
    list_display = ("assignment", "submitted_at")
    list_filter = ("submitted_at",)
    search_fields = ("assignment__title",)
    readonly_fields = ("submitted_at",)


@admin.register(Grading)
class GradingAdmin(admin.ModelAdmin):
    list_display = ("submission", "grade", "graded_at")
    list_filter = ("grade", "graded_at")
    search_fields = ("submission__assignment__title",)
    readonly_fields = ("graded_at",)

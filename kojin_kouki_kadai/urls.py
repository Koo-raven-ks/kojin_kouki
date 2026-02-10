from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Lecture URLs
    path("lectures/", views.LectureListView.as_view(), name="lecture_list"),
    path(
        "lectures/<int:pk>/", views.LectureDetailView.as_view(), name="lecture_detail"
    ),
    path("lectures/new/", views.LectureCreateView.as_view(), name="lecture_create"),
    path(
        "lectures/<int:pk>/edit/",
        views.LectureUpdateView.as_view(),
        name="lecture_update",
    ),
    path(
        "lectures/<int:pk>/delete/",
        views.LectureDeleteView.as_view(),
        name="lecture_delete",
    ),
    # Assignment URLs
    path("assignments/", views.AssignmentListView.as_view(), name="assignment_list"),
    path(
        "assignments/<int:pk>/",
        views.AssignmentDetailView.as_view(),
        name="assignment_detail",
    ),
    path(
        "assignments/new/",
        views.AssignmentCreateView.as_view(),
        name="assignment_create",
    ),
    path(
        "assignments/<int:pk>/edit/",
        views.AssignmentUpdateView.as_view(),
        name="assignment_update",
    ),
    path(
        "assignments/<int:pk>/delete/",
        views.AssignmentDeleteView.as_view(),
        name="assignment_delete",
    ),
    # SubmissionRecord URLs
    path(
        "assignments/<int:assignment_id>/submission/new/",
        views.SubmissionRecordCreateView.as_view(),
        name="submission_create",
    ),
    path(
        "submissions/<int:pk>/edit/",
        views.SubmissionRecordUpdateView.as_view(),
        name="submission_update",
    ),
    path(
        "submissions/<int:pk>/delete/",
        views.SubmissionRecordDeleteView.as_view(),
        name="submission_delete",
    ),
    # Grading URLs（先生用）
    path(
        "submissions/<int:submission_id>/grading/new/",
        views.GradingCreateView.as_view(),
        name="grading_create",
    ),
    path(
        "gradings/<int:pk>/edit/",
        views.GradingUpdateView.as_view(),
        name="grading_update",
    ),
    path(
        "gradings/<int:pk>/delete/",
        views.GradingDeleteView.as_view(),
        name="grading_delete",
    ),
]

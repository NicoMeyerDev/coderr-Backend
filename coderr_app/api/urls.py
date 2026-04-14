from django.urls import path
from .views import OfferView, OfferSingleView

urlpatterns = [

    #Offers
    path("offers/", OfferView.as_view(), name="offer-list-create"),
    path("offers/<int:pk>/", OfferSingleView.as_view(), name="offer-detail"),

    #  #Tasks
    # path("tasks/", TaskView.as_view()),
    # path("tasks/<int:pk>/", TaskSingleView.as_view(), name="task-detail"),
    # path("tasks/assigned-to-me/", AssignedToMeView.as_view()),
    # path("tasks/reviewing/", ReviewingView.as_view()),

    # #Comments
    # path("tasks/<int:task_id>/comments/", CommentView.as_view()),
    # path("tasks/<int:task_id>/comments/<int:comment_id>/", CommentSingleView.as_view()),

    #  #Email
    # path("email-check/", EmailCheckView.as_view(), name="email-check"),
]
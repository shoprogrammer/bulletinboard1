from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    #一段階目スレッド
    path('boardlist/',views.boardlist,name="board-list"),
    path('boardnew/',login_required(views.boardnew),name="board-new"),
    path('boardcreate/',login_required(views.boardcreate),name="board-create"),
    path('boarddetail/<int:pk>',views.boarddetail,name="board-detail"),
    path('boardupdate/<int:pk>',login_required(views.boardupdate),name="board-update"),
    path('boarddelete/<int:pk>',login_required(views.boarddelete),name='board-delete'),
    path('my_boards/',login_required(views.my_boards),name="my_boards"),


    #二段階目コメント
    path('comment/<int:pk>/',login_required(views.comment_create),name="comment-create"),
    path('comment/<int:board_pk>/delete/<int:comment_pk>/',login_required(views.comment_delete),name="comment-delete"),

    #三段階目コメント
    path('comment/<int:board_pk>/detail/<int:comment_pk>/',views.comment_detail,name='comment-detail'),
    path('comment/<int:board_pk>/reaction/<int:comment_pk>/',views.reaction_create,name='reaction-create'),
    path('comment/<int:board_pk>/reaction/<int:comment_pk>/delete/<int:reaction_pk>/',views.reaction_delete,name="reaction-delete"),

    #検索機能の追加
    path('search/',views.board_search,name='search'),

    #並び替え機能
    path('sort/',views.board_sort,name='sort'),

    # favorite
    path('add_favorite/',views.add_favorite,name='add_favorite'),
    path('remove_favorite/',views.remove_favorite,name='remove_favorite'),
    path('display_favorite',views.display_favorite,name='display_favorite'),

    #お問合せフォーム
    path('contact/',views.contact,name="contact"),
    path('contact/success/',views.contact_success,name="contact_success")



]

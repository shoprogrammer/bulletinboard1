from django.shortcuts import render,redirect,get_object_or_404
from .models import BoardModel,Comment,Reaction,Favorite
from .forms import BoardForm,SignUpForm,CommentForm,ReactionForm,FavoriteForm,ContactForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.db.models import Count
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages

def user_owns_board(view_func):
    @wraps(view_func)
    def wrapper(request,pk):
        board = get_object_or_404(BoardModel,pk=pk)
        if board.user == request.user:
            return view_func(request,pk)
        else:
            return redirect('board-list')
    return wrapper




def boardlist(request):
    template_name='bulletin/boardlist.html'
    user = request.user

    if user.is_authenticated:
        boards_query = BoardModel.objects.annotate(is_favorite=Count('favorite',filter=models.Q(favorite__user=user))).order_by('-updated_at')
    else:
        boards_query = BoardModel.objects.all().order_by('updated_at')

    paginator = Paginator(boards_query,6)
    page_number = request.GET.get('page')
    boards = paginator.get_page(page_number)


    return render(request,template_name,{'boards':boards})



@login_required
def boardnew(request):
    template_name='bulletin/boardnew.html'
    form = BoardForm()



    return render(request,template_name,{"form":form})

@login_required
def boardcreate(request):
    template_name='bulletion/boardnew.html'
    if request.POST:
        form = BoardForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

            messages.success(request,'掲示板の投稿に成功しました')
            
            return redirect('board-list')
        
        else:
            messages.error(request,'掲示板の投稿に失敗しました')

    else:
        form = BoardForm()


    return render(request,template_name,{"form":form})

# @login_required
# @user_owns_board
def boarddetail(request,pk):
    template_name='bulletin/boarddetail.html'
    
    # board = BoardModel.objects.get(pk=pk)
    #test
    board = get_object_or_404(BoardModel,pk=pk)


    #コメント表示
    comments_query = Comment.objects.filter(board=pk).order_by('-created_at')

    comment_form = CommentForm()

    # paginatorのtest
    answer=0
    paginator = Paginator(comments_query,3)
    if comments_query.count() == 3:
        answer = "maxになりました"
        current_level = messages.get_level(request)
        print(current_level)
        messages.info(request,'この掲示板は、もう使えません')
   

    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)



    return render(request,template_name,{"board":board,"comments":comments,"comment_form":comment_form,"answer":answer})

@login_required
@user_owns_board
def boardupdate(request,pk):
    template_name='bulletin/boardupdate.html'
    board = BoardModel.objects.get(pk=pk)
    if request.POST:
        form = BoardForm(request.POST,instance=board)
        if form.is_valid():
            form.save()
            return redirect('board-list')
    else:
        form = BoardForm(instance=board)
    return render(request,template_name,{'form':form,'board':board})


@login_required
@user_owns_board
def boarddelete(request,pk):
    board = BoardModel.objects.get(pk=pk)
    if request.POST:
        board.delete()
        return redirect('board-list')
    return redirect('board-list')


@login_required
def my_boards(request):
    template_name = 'bulletin/my_boards.html'
    user = request.user
    boards = user.boards.all()
    return render(request,template_name,{'boards':boards})


@login_required
def comment_create(request,pk):
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.instance.user =  request.user
            comment_form.instance.board_id = pk
            comment_form.save()
        
            messages.success(request,'掲示板の投稿に成功しました')
            
        else:
            messages.error(request,'掲示板の投稿に失敗しました')

    return redirect("board-detail",pk=pk)

@login_required
def comment_delete(request,board_pk,comment_pk):
    comment = get_object_or_404(Comment,pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('board-detail',pk=board_pk)

@login_required
def comment_detail(request,board_pk,comment_pk):
    template_name = 'reaction/reactionnew.html'
    board = BoardModel.objects.get(pk=board_pk)
    comment = Comment.objects.get(pk=comment_pk)
    
    #reactionの表示
    reactions_query = Reaction.objects.filter(board=board,comment=comment).order_by('-created_at')
    reaction_form = ReactionForm()
    
    #paginator test
    paginator = Paginator(reactions_query,3)
    if reactions_query.count() >= 3:
        messages.info(request,'投稿が３を超えたため、このコメントはもう使えません')
        comment.delete()
        return redirect('board-detail', board.pk)

    page_number = request.GET.get('page')
    reactions = paginator.get_page(page_number)


    return render(request,template_name,{"comment":comment,"board":board,"reactions":reactions,"reaction_form":reaction_form})
    
#reactionの作成
def reaction_create(request,board_pk,comment_pk):
    template_name = 'reaction/reactionnew.html'

    board = BoardModel.objects.get(pk=board_pk)
    comment = Comment.objects.get(pk=comment_pk)

    if request.POST:
        reaction_form = ReactionForm(request.POST)
        if reaction_form.is_valid():
            reaction_form.instance.user = request.user
            reaction_form.instance.board_id = board_pk
            reaction_form.instance.comment_id = comment_pk
            reaction_form.save()
    else:
        reaction_form = ReactionForm()   

    return redirect('comment-detail',board_pk=board_pk,comment_pk=comment_pk)

    # return render(request,template_name,{"reaction_form":reaction_form,"board":board,"comment":comment})


#reactionの削除
def reaction_delete(request,board_pk,comment_pk,reaction_pk):
    reaction = Reaction.objects.get(pk=reaction_pk)
    if request.user == reaction.user:
        reaction.delete()

    return redirect('comment-detail',board_pk=board_pk,comment_pk=comment_pk)







#検索機能
def board_search(request):
    template_name = 'bulletin/boardlist.html'
    query = request.GET.get('query')
    search_type = request.GET.get('search_type')
    boards = BoardModel.objects.all()

    if search_type == 'partial':
        boards = boards.filter(title__icontains=query)
    elif search_type == 'prefix':
        boards = boards.filter(title__startswith=query)
    elif search_type == 'suffix':
        boards = boards.filter(title__endswith=query)
    else:
        boards = boards.filter(title__icontains=query)

    return render(request,template_name,{'boards':boards})


#並び替え機能
def board_sort(request):
    template_name = 'bulletin/boardlist.html'

    sort_by = request.GET.get('sort')
    direction = request.GET.get('direction')

    if direction == 'asc':
        next_direction = 'desc'
    else:
        next_direction = 'asc'

    if sort_by:
        if direction == 'desc':
            boards = BoardModel.objects.all().order_by(f'-{sort_by}')
        else:
            boards = BoardModel.objects.all().order_by(f'{sort_by}')
    else:
        boards = BoardModel.objects.all()

    context = {
        'boards':boards,
        'sort_by':sort_by,
        'direction':direction,
        'next_direction':next_direction,


    }



    return render(request,template_name,context)


@login_required
def add_favorite(request):
    if request.POST:
        form = FavoriteForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('board-list')
    return redirect('board-list')

@login_required
def remove_favorite(request):
    if request.POST:
        favorite = Favorite.objects.get(user=request.user,board=request.POST.get('board'))
        favorite.delete()
        return redirect('board-list')
    return redirect('board-list')

#自分のお気に入りを表示
@login_required
def display_favorite(request):
    template_name = 'bulletin/my_favoriteboards.html'
    favorites = Favorite.objects.all()
    return render(request,template_name,{"favorites":favorites})






#お問合せフォーム
def contact(request):
    template_name = 'inquiry/contact.html'
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

        # ユーザーへのメール
            user_subject = 'お問い合わせを受け付けました'
            user_message = 'お問合せ内容:¥n¥n{}'.format(contact.message)
            send_mail(user_subject,user_message,settings.EMAIL_HOST_USER,[contact.email])
        #運営者へのメール
            admin_subject = 'お問い合わせがありました'
            admin_message = 'お問合せ内容:¥n¥n{}'.format(contact.message)
            send_mail(admin_subject,admin_message,settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER])
            return redirect('contact-success')
    else:
        form = ContactForm()

    return render(request,template_name,{'form':form})






def contact_success(request):
    template_name = 'inquiry/contact_success.html'
    return render(request,template_name)



#ログインページのビュー
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'





#ログアウト
def logout_view(request):
    
    logout(request)
    return redirect('board-list')

#サインアップページのビュー
def signup(request):
    template_name = 'registration/signup.html'
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = SignUpForm()

    return render(request,template_name,{"form":form})







#プロフィールページのビュ
@login_required
def profile(request):
    template_name = 'accounts/profile.html'
    user = request.user
    return render(request,template_name,{"user":user})
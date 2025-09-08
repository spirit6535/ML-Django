from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.forms.news_form import NewsForm
from app.models import News



@login_required

def index(request):
    # Получаем все новости из базы данных
    news_list = News.objects.all().order_by('-created_at')  # Сортировка по дате (новые сверху)
    return render(request, 'app/index.html', {'news_list': news_list})

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user  # Устанавливаем автора
            news.save()
            return redirect('app:index')
    else:
        form = NewsForm()
    return render(request, 'app/add_news.html', {'form': form})


def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    # Проверяем, что текущий пользователь - автор новости
    if news.author != request.user:
        return redirect('app:index')  # Или покажите сообщение об ошибке

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('app:index')
    else:
        form = NewsForm(instance=news)

    return render(request, 'app/edit_news.html', {'form': form, 'news': news})


@login_required
def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)

    # Проверяем, что текущий пользователь - автор новости
    if news.author != request.user:
        return redirect('app:index')  # Или покажите сообщение об ошибке

    if request.method == 'POST':
        news.delete()
        return redirect('app:index')

    return render(request, 'app/delete_news.html', {'news': news})

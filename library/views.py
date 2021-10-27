from django.shortcuts import render, redirect
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Record, Book, Search
from .converter import speech_txt, book_reader
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.core.files import File
import os


@login_required(login_url='veriuser:login')
def index(request):
    return render(request, 'home.html', {
    })


@login_required(login_url='veriuser:login')
def books(request):
    return render(request, 'books.html', {
        'books': Book.objects.all(),
    })

@login_required(login_url='veriuser:login')
def add_book(request):
    context = {}
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book successfully added')
            return redirect('library:add_book')
        else:
            context['form'] = form
            context['error'] ='invalid input'
            return render(request, "add_book.html", context)
    else:
        form = BookForm()
        context['form'] = form
        return render(request, "add_book.html", context)


@login_required(login_url='veriuser:login')
def delete_record(request,id):
    _record= get_object_or_404(Record,id=id)
    _record.delete()
    return redirect('library:record_list')


@login_required(login_url='veriuser:login')
def play_book(request,id):
    results = book_reader(id)
    if results['status'] == 'success':
        return render(request, 'book_reader.html', {})
    else:
        e = results['e']
        #return redirect('library:error',e)
        context={'e':results['e']}
        return render(request, "error.html", context)

@login_required(login_url='veriuser:login')
def record(request):
    if request.method == "POST":
        language = request.POST.get("language")
        audio_file = request.FILES.get("recorded_audio")
        _record = Record(language=language, voice_record=audio_file, user=request.user)
        _record.save()
        results = speech_txt(_record.voice_record.url,language)
        if results['status'] == 'success':
            _record = Record(language=language, voice_record=audio_file, user=request.user, pdf=results['my_text'])
            _record.save()
        else:
            return redirect('library:error', results['e'])
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse(
            {
                "url": _record.get_absolute_url(),
                "success": True,
            }
        )
    context = {"page_title": "Record audio"}
    return render(request, "record.html", context)

@login_required(login_url='veriuser:login')
def record_detail(request, id):
    _record = get_object_or_404(Record, id=id)
    context = {
        "page_title": "Recorded audio detail",
        "record": _record,
    }
    return render(request, 'record_detail.html', context)
    #return FileResponse(open('f.pdf', 'rb'), as_attachment=True, content_type='application/pdf')


@login_required(login_url='veriuser:login')
def record_list(request):
    context = {}
    records = Record.objects.filter(user=request.user)
    if records.count() == 0:
        context['empty'] = 'You have no previous voice records '
        return render(request, 'record_list.html', context)
    else:
        paginator = Paginator(records, 10)
        page = request.GET.get('page')
        results = paginator.get_page(page)
        context['results'] = results
        return render(request, 'record_list.html', context)


@login_required(login_url='veriuser:login')
def previous_search(request):
    context = {}
    searches = Search.objects.filter(user=request.user)
    if searches.count() == 0:
        context['empty'] = 'You have no previous search records '
        return render(request, 'previous_search.html', context)
    else:
        paginator = Paginator(searches, 9)
        page = request.GET.get('page')
        results = paginator.get_page(page)
        context['results'] = results
        return render(request, 'previous_search.html', context)


@login_required(login_url='veriuser:login')
def search(request):
    context = {}
    if request.method == "POST":
        audio_file = request.FILES.get("recorded_audio")
        language = request.POST.get("language")
        _search = Search(voice_record=audio_file, user=request.user, language=language)
        _search.save()
        messages.success(request, "Audio recording successfully added!")
        return JsonResponse(
            {
                "url": _search.get_results_url(),
                "success": True,
            }
        )
    context = {"page_title": "Record audio"}#don't touch
    return render(request, "search.html", context)


@login_required(login_url='veriuser:login')
def search_result(request, id):
    context = {}
    _search = get_object_or_404(Search, id=id)
    voice_note = _search.voice_record.url
    language = _search.language
    results = speech_txt(voice_note, language)
    if results['status'] == 'success':
        my_text = results['my_text']
        queryset = (Q(title__icontains=my_text) | Q(description__icontains=my_text))
        results = Book.objects.filter(queryset).distinct()

        if results.count() == 0:
            context['question'] = my_text
            context['no_result'] = 'no results found for this search: '+my_text
            return render(request, 'search_results.html', context)
        else:
            paginator = Paginator(results, 9)
            page = request.GET.get('page')
            results = paginator.get_page(page)
            context['question'] = my_text
            context['results'] = results
            return render(request, 'search_results.html', context)
    else:
        return redirect('library:error', results['e'])


@login_required(login_url='veriuser:login')
def search_detail(request, id):
    record = get_object_or_404(Record, id=id)
    context = {
        "page_title": "Recorded audio detail",
        "record": record,
    }
    return render(request, "record_detail.html", context)


@login_required(login_url='veriuser:login')
def delete_search(request,id):
    _search = get_object_or_404(Search, id=id)
    _search.delete()
    return redirect('library:previous_search')


@login_required(login_url='veriuser:login')
def error(request, e):
    context = {'e':e}
    return render(request, "error.html", context)


@login_required(login_url='veriuser:login')
def search_bar(request):
    context = {}
    my_text = request.GET.get('sch', '')
    queryset = (Q(title__icontains=my_text) | Q(description__icontains=my_text))
    results = Book.objects.filter(queryset).distinct()

    if results.count() == 0:
        context['question'] = my_text
        context['no_result'] = 'no results found for this search: '+my_text
    else:
        paginator = Paginator(results, 9)
        page = request.GET.get('page')
        results = paginator.get_page(page)
        context['question'] = my_text
        context['results'] = results
    return render(request, 'search_results.html', context)
    
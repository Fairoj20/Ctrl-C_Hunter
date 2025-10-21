
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import TextEntry, ComparisonHistory
from .forms import TextEntryForm, CompareForm
from .utils import extract_text_from_file, compute_similarity, normalize_text

from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'checker/home.html')


class EntryListView(generic.ListView):
    model = TextEntry
    template_name = 'checker/entry_list.html'
    context_object_name = 'entries'


class EntryDetailView(generic.DetailView):
    model = TextEntry
    template_name = 'checker/entry_detail.html'
    context_object_name = 'entry'


class EntryCreateView(generic.CreateView):
    model = TextEntry
    form_class = TextEntryForm
    template_name = 'checker/entry_form.html'
    success_url = reverse_lazy('checker:entry_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        # populate extracted_text after save
        entry = self.object
        f = form.cleaned_data.get('uploaded_file')
        pasted = form.cleaned_data.get('pasted_text')
        if f:
            text = extract_text_from_file(f, getattr(f, 'name', None))
            entry.extracted_text = normalize_text(text)
        else:
            entry.extracted_text = normalize_text(pasted)
        entry.save()
        return resp


class EntryUpdateView(generic.UpdateView):
    model = TextEntry
    form_class = TextEntryForm
    template_name = 'checker/entry_form.html'
    success_url = reverse_lazy('checker:entry_list')

    def form_valid(self, form):
        resp = super().form_valid(form)
        entry = self.object
        f = form.cleaned_data.get('uploaded_file')
        pasted = form.cleaned_data.get('pasted_text')
        if f:
            text = extract_text_from_file(f, getattr(f, 'name', None))
            entry.extracted_text = normalize_text(text)
        else:
            entry.extracted_text = normalize_text(pasted)
        entry.save()
        return resp


class EntryDeleteView(generic.DeleteView):
    model = TextEntry
    template_name = 'checker/entry_confirm_delete.html'
    success_url = reverse_lazy('checker:entry_list')


def compare_view(request):
    """
    Compare two sources: either choose existing entries, upload files, or paste texts.
    Display similarity result.
    """
    # ALWAYS print this, even on GET request
    print("\n" + "=" * 50)
    print("COMPARE VIEW CALLED!")
    print(f"Request method: {request.method}")
    print("=" * 50 + "\n")

    result = None
    if request.method == 'POST':
        print("POST request detected!")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")

        form = CompareForm(request.POST, request.FILES)

        # DEBUG: Check if form is valid
        print("=" * 50)
        print("Form submitted!")
        print(f"Form is valid: {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        print("=" * 50)

        if form.is_valid():
            # Determine text A - PRIORITIZE pasted text, then file, then entry
            pasted_a = form.cleaned_data.get('pasted_a', '').strip()
            file_a = form.cleaned_data.get('file_a')
            entry_a = form.cleaned_data.get('entry_a')

            if pasted_a:
                a_text = pasted_a
                print("Using pasted text A")
            elif file_a:
                a_text = extract_text_from_file(file_a, getattr(file_a, 'name', None))
                print("Using uploaded file A")
            elif entry_a:
                a_text = entry_a.extracted_text
                print("Using selected entry A")
            else:
                a_text = ''
                print("No text A provided")

            # Determine text B - PRIORITIZE pasted text, then file, then entry
            pasted_b = form.cleaned_data.get('pasted_b', '').strip()
            file_b = form.cleaned_data.get('file_b')
            entry_b = form.cleaned_data.get('entry_b')

            if pasted_b:
                b_text = pasted_b
                print("Using pasted text B")
            elif file_b:
                b_text = extract_text_from_file(file_b, getattr(file_b, 'name', None))
                print("Using uploaded file B")
            elif entry_b:
                b_text = entry_b.extracted_text
                print("Using selected entry B")
            else:
                b_text = ''
                print("No text B provided")

            # DEBUG: Print what we're comparing
            print("=" * 50)
            print(f"Text A length: {len(a_text)}")
            print(f"Text A preview: {a_text[:200]}")
            print(f"Text B length: {len(b_text)}")
            print(f"Text B preview: {b_text[:200]}")
            print("=" * 50)

            # Calculate similarity
            score, status = compute_similarity(a_text, b_text)

            print(f"Raw score: {score}")
            print(f"Status: {status}")

            # Convert score from 0.0-1.0 to 0-100 percentage
            score_percentage = round(score * 100, 2)
            print(f"Percentage: {score_percentage}")
            print("=" * 50)

            result = {
                'score': score_percentage,
                'status': status,
                'text_a_snippet': (a_text or '')[:1000],
                'text_b_snippet': (b_text or '')[:1000],
            }

            # Save to comparison history
            ComparisonHistory.objects.create(
                source_a_type='entry' if entry_a else ('file' if file_a else 'pasted'),
                source_a_entry=entry_a,
                source_a_text=a_text[:5000],  # Store first 5000 chars
                source_a_filename=getattr(file_a, 'name', '') if file_a else '',

                source_b_type='entry' if entry_b else ('file' if file_b else 'pasted'),
                source_b_entry=entry_b,
                source_b_text=b_text[:5000],  # Store first 5000 chars
                source_b_filename=getattr(file_b, 'name', '') if file_b else '',

                similarity_score=score_percentage,
                similarity_status=status,
            )
            print("Comparison saved to history!")

            # Optionally: store results if user selected entries
            if entry_a and entry_b:
                entry_a.last_compared_with = entry_b
                entry_a.last_similarity_score = score_percentage
                entry_a.last_similarity_status = status
                entry_a.save()
    else:
        form = CompareForm()

    return render(request, 'checker/compare.html', {'form': form, 'result': result})


class ComparisonHistoryListView(generic.ListView):
    model = ComparisonHistory
    template_name = 'checker/history_list.html'
    context_object_name = 'comparisons'
    paginate_by = 20  # Show 20 comparisons per page


class ComparisonHistoryDetailView(generic.DetailView):
    model = ComparisonHistory
    template_name = 'checker/history_detail.html'
    context_object_name = 'comparison'


class ComparisonHistoryDeleteView(generic.DeleteView):
    model = ComparisonHistory
    template_name = 'checker/history_confirm_delete.html'
    success_url = reverse_lazy('checker:history_list')
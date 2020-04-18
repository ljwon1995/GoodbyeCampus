from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect, Http404
from django.db.models import Sum

from .models import Candidate, Poll, Choice
import datetime

# Create your views here.
def index(request):
	candidates = Candidate.objects.all()
	context = {'candidates':candidates}
	return render(request, 'elections/index.html',context)

def areas(request, area):
	today = datetime.datetime.now()
	print(today)	

	try:	
		poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte = today)
		candidates = Candidate.objects.filter(area = area)
	except:
		poll = None
		candidates = None

	context = {'candidates': candidates, 'area': area, 'poll': poll}
	return render(request,'elections/areas.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    print(poll_id + 1)
    selection = request.POST['choice']

    try: 
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def candidates(request, name):
	candidate = get_object_or_404(Candidate, name=name)
	# try:
	# 	candidate = Candidate.objects.get(name=name)
	# except:
	# 	raise Http404

	return HttpResponse(candidate.name)

def results(request, area):
	candidates = Candidate.objects.filter(area = area)
	
	polls = Poll.objects.filter(area = area)
	polls_result = []
	for poll in polls:
		result = {}
		result['start_date'] = poll.start_date
		result['end_date'] = poll.end_date
		total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))
		result['total_votes'] = total_votes['votes__sum']
		rates = []
		for candidate in candidates:
			try:
				choice = Choice.objects.get(poll_id=poll.id, candidate_id=candidate.id)
				rates.append(round(choice.votes * 100/result['total_votes'],1))
			except:
				rates.append(0)
		result['rates'] = rates

		polls_result.append(result)

	context = {'candidates':candidates, 'area':area, 'polls_result':polls_result}
	return render(request, 'elections/result.html', context)

from .models import LeaderBoard, Score, KnockOutTeamSelection
from django.contrib.auth import get_user_model


def update_leaderboard():
	users = get_user_model().objects.all()
	for usr in users:
		try:
			point = 0
			scores = Score.objects.filter(owner=usr)
			kopred = KnockOutTeamSelection.objects.get(owner=usr)
			lb = LeaderBoard.objects.get(owner=usr)

			for scr in scores:
				point += scr.mypoints

			point += (kopred.qfpoints + kopred.sfpoints + kopred.fpoints + kopred.champpoints)

			lb.points = point
			lb.save()
		except:
			pass

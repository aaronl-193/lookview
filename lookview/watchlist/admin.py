from django.contrib import admin

import watchlist.models as models

admin.site.register(models.Watchlist)
admin.site.register(models.WatchlistFilm)

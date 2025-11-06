import datetime

from django.contrib import admin
from .models import Article, Admins, FakeDetection


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_fake', 'is_published', 'date_updated')
    list_filter = ('is_fake', 'is_published')

    def save_model(self, request, obj, form, change):
        """
        Overrides the save_model method to log changes in the Admins model
        when is_fake or is_published is modified.
        """
        # Get the original article from the database before saving
        if change:
            old_obj = Article.objects.get(pk=obj.pk)

            # Check if 'is_fake' or 'is_published' changed
            if old_obj.is_fake != obj.is_fake or old_obj.is_published != obj.is_published:
                # Create an entry in Admins table

                reported = False
                if obj.is_fake:
                    reported = True
                    if obj.is_published:
                        description = 'Flagged as Fake, So not Published'
                    else:
                        description = 'Flagged as Fake'
                else:
                    if obj.is_published:
                        obj.date_published =datetime.date.today()
                        obj.save()
                        description = 'News considered as Real, So Published '
                    else:
                        description = 'Want to publish'
                Admins.objects.get_or_create(
                    article=obj,
                    user=request.user,  # Admin making the change
                    is_published=obj.is_published,
                    is_reported=reported,  # Change as needed
                    updated_date=obj.date_updated,
                    description=description
                )

        # Save the updated article
        super().save_model(request, obj, form, change)


# Register models with the admin panel
admin.site.register(Article, ArticleAdmin)
admin.site.register(Admins)
admin.site.register(FakeDetection)

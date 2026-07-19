import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Inkspire.settings")
django.setup()

from BlogApp.models import Blogs
from django.conf import settings
from django.core.files import File

uploaded = 0
failed = 0
skipped = 0

for blog in Blogs.objects.all():

    if not blog.blog_image:
        skipped += 1
        continue

    # Original relative path stored in DB
    relative_path = blog.blog_image.name

    # Build the local file path
    local_file = os.path.join(settings.MEDIA_ROOT, relative_path)

    if not os.path.exists(local_file):
        print(f"❌ Missing: {local_file}")
        failed += 1
        continue

    try:
        print(f"Uploading: {blog.title}")

        with open(local_file, "rb") as f:
            blog.blog_image.save(
                os.path.basename(relative_path),
                File(f),
                save=True,
            )

        uploaded += 1
        print("✅ Uploaded")

    except Exception as e:
        failed += 1
        print(e)

print("\nFinished")
print(f"Uploaded : {uploaded}")
print(f"Skipped  : {skipped}")
print(f"Failed   : {failed}")
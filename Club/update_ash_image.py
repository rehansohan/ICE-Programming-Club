import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Club.settings')
django.setup()

from Core.models import CommunityMember

# Find Ashraful Islam
member = CommunityMember.objects.filter(name__icontains='Ashraful').first()

if member:
    print(f"Found: {member.name}")
    print(f"Current image: {member.image.name if member.image else 'No image'}")
    
    # Update to use circular image
    member.image = 'community/ash_circular.png'
    member.save()
    print(f"✓ Updated to: {member.image.name}")
else:
    print("Member not found. Available members:")
    for m in CommunityMember.objects.all():
        print(f"  - {m.name}: {m.image.name if m.image else 'No image'}")

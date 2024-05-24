from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("user", MenuItem("Blog", reverse('blog_list'), icon='flaticon-graphic-1', weight=1))
Menu.add_item("user", MenuItem("Private Blog", reverse('private_blog_list'), icon='flaticon-graphic-1', weight=1))

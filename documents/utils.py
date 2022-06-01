from .models import Category, Document


def get_child_categories(category: Category):
    sub_categories = {}
    for sub_category in Category.objects.filter(parent=category).all():
        sub_categories[sub_category.name] = {
            'category_id': sub_category.id,
            'child_categories': get_child_categories(sub_category),
        }
    return sub_categories


def get_documents_by_categories_tree():
    documents_by_categories = {}
    for main_category in Category.objects.filter(parent=None).all():
        documents_by_categories[main_category.name] = {
            'category_id': main_category.id,
            'child_categories': get_child_categories(main_category),
        }
    return documents_by_categories


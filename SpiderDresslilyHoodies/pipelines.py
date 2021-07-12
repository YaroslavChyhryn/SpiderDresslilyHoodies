class SpiderdresslilyhoodiesPipeline:
    """
    This Pipeline make field blank by default
    """
    def process_item(self, item, spider):
        item.setdefault('discount', 0)
        item.setdefault('discounted_price', 0)
        item.setdefault('total_reviews', 0)
        return item

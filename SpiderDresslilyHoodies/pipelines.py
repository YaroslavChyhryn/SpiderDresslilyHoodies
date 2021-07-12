class SpiderdresslilyhoodiesPipeline:
    """
    This Pipeline make field blank by default
    """
    def process_item(self, item, spider):
        for field in item.fields:
            # not shure how identify null object in csv
            item.setdefault(field, '')
        return item

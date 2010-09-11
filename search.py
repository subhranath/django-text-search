import re

def get_keywords(query_string):
    """Accepts a search query string and returns a list of search keywords.
    """
    # Regex to split on double-quotes, single-quotes, and continuous
    # non-whitespace characters.
    split_pattern = re.compile('("[^"]+"|\'[^\']+\'|\S+)')
    
    # Pattern to remove more than one inter white-spaces.
    remove_inter_spaces_pattern = re.compile('[\s]{2,}')
    
    # Return the list of keywords.
    return [remove_inter_spaces_pattern.sub(' ', t.strip(' "\'')) \
            for t in split_pattern.findall(query_string) \
            if len(t.strip(' "\'')) > 0]

def get_results(objects, query, field_list):
    """Returns a QuerySet of filtered objects based on the 'query',
    upon a QuerySet of 'objects', on the fields specified by the list
    'field_list'.
    """
    
    # Create a string representing the actual query condition for filtering.
    condition = ''
    for field in field_list:
        condition = condition + 're.compile(query_pattern).search(obj.%(field)s) or ' % {'field': field}
    condition = condition[:-4]
    
    # Apply the query condition for all the keywords.
    for keyword in get_keywords(query):
        # List where the partially filtered object ids are stored.
        filtered_ids = []
        
        # Check for the filter condition for the current keyword, on all the presently filtered objects. 
        for obj in objects:
            
            # Check for the filtering.
            query_pattern = re.compile(keyword, re.IGNORECASE)
            if eval(condition):
                filtered_ids.append(obj.id)
        
        # For the next iteration work with the currently filtered objects only.
        objects = objects.filter(id__in=filtered_ids)
        
    return objects

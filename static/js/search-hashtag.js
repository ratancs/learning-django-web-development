var hashTags = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('query'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: '../../hashtag.json?query=%QUERY'
});

hashTags.initialize();

$('.search-hash-tag-query').typeahead(null, {
  displayKey: 'query',
  source: hashTags.ttAdapter()
});

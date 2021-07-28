/* Cite a dataset in a specific citation style
*/
ckan.module('show-citation', function (jQuery) {
  return {
    options: {
      url: window.location.href
    },
    initialize: function () {
      var self = this;

      $.proxyAll(this, /setup/, /_on/);

      this.citation = this.el.data('citation');
      this.record = this.el.parent().next('div');
      this.clipboard = this.record.next();
      var clipboardJS = new ClipboardJS(this.clipboard.find('.btn')[0]);

      clipboardJS.on('success', function(e) {
        e.clearSelection();
      });

      this.setupCitation();

      jQuery.getJSON('/ckanext/citation/csl/csl_styles.json').done(
        function(data) {
          self.setupSelection(data);
        })
      .fail(
        function(jqXHR, textStatus, errorThrown) {
          this.showError(jqXHR, textStatus, errorThrown);
        }
      );
    },
    setupCitation: function () {
      var version = decodeURIComponent(this.options.url.split('%40')[1]);
      if (version != 'undefined') {
        this.citation.version = version;
      }
      var issued = new Date(this.citation.version);
      var item = {
        'id': this.options.url,
        'type': 'dataset',
        'title': this.citation.title,
        'author': [{'literal': this.citation.author}],
        'issued': {'date-parts': [[issued.getFullYear(),
            issued.getMonth(), issued.getDate()]]},
        'URL': this.options.url,
        'version': this.citation.version
      };

      this.cslJson = {};
      this.cslJson[this.options.url] = item;
    },
    setupSelection: function (data) {
      var self = this;
      var settings = {
        data: data,
        placeholder: 'search',
        width: '100%',
        query: function(q) {
          var that = this;
          var pageSize = 20;
          var results = [];

          if (q.term && q.term !== '') {
            results = _.filter(that.data, function(e) {
              return e.text.toUpperCase().indexOf(q.term.toUpperCase()) >= 0;
            });
          } else if (q.term === '') {
            results = that.data;
          }

          var otherResults = _.filter(results, function(e) {
            return e.category === 'other';
          });
          var slicedResults = otherResults.slice((q.page - 1) * pageSize, q.page * pageSize);

          // Add major styles
          if (q.page === 1) {
             var majorResults = _.filter(results, function(e) {
               return e.category === 'major';
             });
             if (majorResults.length > 0) {
                slicedResults = [{id: 0, text: self._('Major Styles'), children: majorResults, disabled: true}]
                        .concat(slicedResults);
             }
          }
          q.callback({
            results: slicedResults,
            more: otherResults.length >= q.page * pageSize
          });
        }
      };
      var select2 = this.el.select2(settings).select2('data', data[0]);

      this.el.on('select2-selecting', function (e) {
          self.formatStyle(e.object);
      });
      this.formatStyle(data[0]);
    },
    formatStyle: function (style) {
      var self = this;

      self.clipboard.hide();
      jQuery.when(
        jQuery.get(style.href, function(){}, 'text'),
        jQuery.get('/ckanext/citation/csl/locales/locales-en-US.xml', function(){}, 'text'))
      .done(
        function (a1, a2) {
          var citeprocSys = {
            retrieveLocale: function (lang) {return a2[0];},
            retrieveItem: function (id) {return self.cslJson[id];}
          };
          var citeproc = new CSL.Engine(citeprocSys, a1[0]);
          citeproc.updateItems([self.options.url]);
          console.log({citeprocSys});
          console.log(citeproc.makeBibliography());
          self.record.replaceWith(citeproc.makeBibliography()[1].join('\n'));
          self.clipboard.show();
        }
      );
    }
  };
});

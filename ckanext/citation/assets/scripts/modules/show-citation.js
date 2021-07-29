/*
 * Cite a dataset in a specific citation style
 */
ckan.module('show-citation', function ($) {
    return {
        cslJson: {},
        options: {
            url: window.location.href,
            citation: ""
        },
        initialize: function () {
            $.proxyAll(this, /setup/, /_on/);

            this.record = this.el.nextAll('.csl-entry');
            this.clipboard = this.el.nextAll('.btn-group');
            var clipboardJS = new ClipboardJS(this.clipboard.find('.btn')[0]);

            clipboardJS.on('success', function (e) {
                e.clearSelection();
            });
            this.clipboard.show();

            this.setupCitation();
            $.getJSON('/ckanext/citation/csl/csl_styles.json')
                .done(this.setupSelection)
                .fail(this.showError);
        },
        setupCitation: function () {
            var version = decodeURIComponent(this.options.url.split('%40')[1]);
            if (version != 'undefined') {
                this.options.citation.version = version;
            }
            var issued = new Date(this.options.citation.version);
            var item = {
                'id': this.options.url,
                'type': 'dataset',
                'title': this.options.citation.title,
                'author': [{'literal': this.options.citation.author}],
                'issued': {
                    'date-parts': [[issued.getFullYear(),
                    issued.getMonth(), issued.getDate()]]
                },
                'URL': this.options.url,
                'version': this.options.citation.version
            };
            this.cslJson[this.options.url] = item;
        },
        setupSelection: function (data) {
            var self = this;
            var settings = {
                data: data,
                placeholder: 'search',
                width: '100%',
                query: function (q) {
                    var pageSize = 20;
                    var results = [];

                    if (q.term && q.term !== '') {
                        results = _.filter(this.data, function (e) {
                            return e.text.toUpperCase().indexOf(q.term.toUpperCase()) >= 0;
                        });
                    } else if (q.term === '') {
                        results = this.data;
                    }

                    var otherResults = _.filter(results, function (e) {
                        return e.category === 'other';
                    });
                    var slicedResults = otherResults.slice((q.page - 1) * pageSize, q.page * pageSize);

                    // Add major styles
                    if (q.page === 1) {
                        var majorResults = _.filter(results, function (e) {
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

            $.when(
                $.get(style.href, function () {}, 'text'),
                $.get('/ckanext/citation/csl/locales/locales-en-US.xml', function () {}, 'text')
            ).done(
                function (a1, a2) {
                    var citeprocSys = {
                        retrieveLocale: function (lang) {return a2[0];},
                        retrieveItem: function (id) {return self.cslJson[id];}
                    };
                    var citeproc = new CSL.Engine(citeprocSys, a1[0]);
                    citeproc.updateItems([self.options.url]);
                    self.record.replaceWith(citeproc.makeBibliography()[1].join('\n'));
                }
            );
        }
    };
});

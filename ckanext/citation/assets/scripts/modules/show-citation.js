/*
 * Cite a dataset in a specific citation style
 */
ckan.module('show-citation', function ($) {
    return {
        options: {
            url: window.location.href,
            citation: {}
        },
        initialize: function () {
            $.proxyAll(this, /setup/, /_on/);

            this.clipboard = this.el.nextAll('.btn-group');
            this.cslBibBody = this.el.nextAll('.csl-bib-body');
            var clipboardJS = new ClipboardJS(this.clipboard.find('.btn')[0]);

            clipboardJS.on('success', function (e) {
                e.clearSelection();
            });
            this.clipboard.show();

            $.getJSON(this.sandbox.client.url('ckanext/citation/csl/csl_styles.json'))
                .done(this.setupSelection)
                .fail(this.showError);
        },
        setupCitation: function (id) {
            let defaultCSLJson = {
                'id': id,
                'type': 'dataset',
            };
            // Comment because not understand the logic behind
            // let version = decodeURIComponent(this.options.url.split('%40')[1]);
            // if (version != 'undefined') {
            //     defaultCSLJson['version'] = version
            // }
            return {
                ...defaultCSLJson,
                ...this.options.citation
            }
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

            this.sandbox.client.call('POST', 'citation_format_style', {
                style_id: style.id,
                style_dict: self.options.citation,
                style_formatter: 'html'
            }, function (data) {
                self.cslBibBody.children('.csl-entry').remove();
                self.cslBibBody.prepend('<div class="csl-entry">' + data.result + '</div>');
            });
        }
    };
});

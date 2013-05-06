/* Modernizr 2.0.4 (Custom Build) | MIT & BSD
 * Contains: video | iepp | respond | mq | cssclasses | teststyles | testprop | testallprops | prefixes | domprefixes | load
 * Build URL: http://j.mp/m1H1Y1
 */
;
window.Modernizr = function (a, b, c) {
    function D(a, b) {
        var c = a.charAt(0).toUpperCase() + a.substr(1), d = (a + " " + o.join(c + " ") + c).split(" ");
        return C(d, b)
    }

    function C(a, b) {
        for (var d in a)if (k[a[d]] !== c)return b == "pfx" ? a[d] : !0;
        return!1
    }

    function B(a, b) {
        return!!~("" + a).indexOf(b)
    }

    function A(a, b) {
        return typeof a === b
    }

    function z(a, b) {
        return y(n.join(a + ";") + (b || ""))
    }

    function y(a) {
        k.cssText = a
    }

    var d = "2.0.4", e = {}, f = !0, g = b.documentElement, h = b.head || b.getElementsByTagName("head")[0], i = "modernizr", j = b.createElement(i), k = j.style, l, m = Object.prototype.toString, n = " -webkit- -moz- -o- -ms- -khtml- ".split(" "), o = "Webkit Moz O ms Khtml".split(" "), p = {}, q = {}, r = {}, s = [], t = function (a, c, d, e) {
        var f, h, j, k = b.createElement("div");
        if (parseInt(d, 10))while (d--)j = b.createElement("div"), j.id = e ? e[d] : i + (d + 1), k.appendChild(j);
        f = ["&shy;", "<style>", a, "</style>"].join(""), k.id = i, k.innerHTML += f, g.appendChild(k), h = c(k, a), k.parentNode.removeChild(k);
        return!!h
    }, u = function (b) {
        if (a.matchMedia)return matchMedia(b).matches;
        var c;
        t("@media " + b + " { #" + i + " { position: absolute; } }", function (b) {
            c = (a.getComputedStyle ? getComputedStyle(b, null) : b.currentStyle).position == "absolute"
        });
        return c
    }, v, w = {}.hasOwnProperty, x;
    !A(w, c) && !A(w.call, c) ? x = function (a, b) {
        return w.call(a, b)
    } : x = function (a, b) {
        return b in a && A(a.constructor.prototype[b], c)
    }, p.video = function () {
        var a = b.createElement("video"), c = !1;
        try {
            if (c = !!a.canPlayType) {
                c = new Boolean(c), c.ogg = a.canPlayType('video/ogg; codecs="theora"');
                var d = 'video/mp4; codecs="avc1.42E01E';
                c.h264 = a.canPlayType(d + '"') || a.canPlayType(d + ', mp4a.40.2"'), c.webm = a.canPlayType('video/webm; codecs="vp8, vorbis"')
            }
        } catch (e) {
        }
        return c
    };
    for (var E in p)x(p, E) && (v = E.toLowerCase(), e[v] = p[E](), s.push((e[v] ? "" : "no-") + v));
    y(""), j = l = null, a.attachEvent && function () {
        var a = b.createElement("div");
        a.innerHTML = "<elem></elem>";
        return a.childNodes.length !== 1
    }() && function (a, b) {
        function s(a) {
            var b = -1;
            while (++b < g)a.createElement(f[b])
        }

        a.iepp = a.iepp || {};
        var d = a.iepp, e = d.html5elements || "abbr|article|aside|audio|canvas|datalist|details|figcaption|figure|footer|header|hgroup|mark|meter|nav|output|progress|section|summary|time|video", f = e.split("|"), g = f.length, h = new RegExp("(^|\\s)(" + e + ")", "gi"), i = new RegExp("<(/*)(" + e + ")", "gi"), j = /^\s*[\{\}]\s*$/, k = new RegExp("(^|[^\\n]*?\\s)(" + e + ")([^\\n]*)({[\\n\\w\\W]*?})", "gi"), l = b.createDocumentFragment(), m = b.documentElement, n = m.firstChild, o = b.createElement("body"), p = b.createElement("style"), q = /print|all/, r;
        d.getCSS = function (a, b) {
            if (a + "" === c)return"";
            var e = -1, f = a.length, g, h = [];
            while (++e < f) {
                g = a[e];
                if (g.disabled)continue;
                b = g.media || b, q.test(b) && h.push(d.getCSS(g.imports, b), g.cssText), b = "all"
            }
            return h.join("")
        }, d.parseCSS = function (a) {
            var b = [], c;
            while ((c = k.exec(a)) != null)b.push(((j.exec(c[1]) ? "\n" : c[1]) + c[2] + c[3]).replace(h, "$1.iepp_$2") + c[4]);
            return b.join("\n")
        }, d.writeHTML = function () {
            var a = -1;
            r = r || b.body;
            while (++a < g) {
                var c = b.getElementsByTagName(f[a]), d = c.length, e = -1;
                while (++e < d)c[e].className.indexOf("iepp_") < 0 && (c[e].className += " iepp_" + f[a])
            }
            l.appendChild(r), m.appendChild(o), o.className = r.className, o.id = r.id, o.innerHTML = r.innerHTML.replace(i, "<$1font")
        }, d._beforePrint = function () {
            p.styleSheet.cssText = d.parseCSS(d.getCSS(b.styleSheets, "all")), d.writeHTML()
        }, d.restoreHTML = function () {
            o.innerHTML = "", m.removeChild(o), m.appendChild(r)
        }, d._afterPrint = function () {
            d.restoreHTML(), p.styleSheet.cssText = ""
        }, s(b), s(l);
        d.disablePP || (n.insertBefore(p, n.firstChild), p.media = "print", p.className = "iepp-printshim", a.attachEvent("onbeforeprint", d._beforePrint), a.attachEvent("onafterprint", d._afterPrint))
    }(a, b), e._version = d, e._prefixes = n, e._domPrefixes = o, e.mq = u, e.testProp = function (a) {
        return C([a])
    }, e.testAllProps = D, e.testStyles = t, g.className = g.className.replace(/\bno-js\b/, "") + (f ? " js " + s.join(" ") : "");
    return e
}(this, this.document), function (a, b) {
    function u() {
        r(!0)
    }

    a.respond = {}, respond.update = function () {
    }, respond.mediaQueriesSupported = b;
    if (!b) {
        var c = a.document, d = c.documentElement, e = [], f = [], g = [], h = {}, i = 30, j = c.getElementsByTagName("head")[0] || d, k = j.getElementsByTagName("link"), l = [], m = function () {
            var b = k, c = b.length, d = 0, e, f, g, i;
            for (; d < c; d++)e = b[d], f = e.href, g = e.media, i = e.rel && e.rel.toLowerCase() === "stylesheet", !!f && i && !h[f] && (!/^([a-zA-Z]+?:(\/\/)?(www\.)?)/.test(f) || f.replace(RegExp.$1, "").split("/")[0] === a.location.host ? l.push({href: f, media: g}) : h[f] = !0);
            n()
        }, n = function () {
            if (l.length) {
                var a = l.shift();
                s(a.href, function (b) {
                    o(b, a.href, a.media), h[a.href] = !0, n()
                })
            }
        }, o = function (a, b, c) {
            var d = a.match(/@media[^\{]+\{([^\{\}]+\{[^\}\{]+\})+/gi), g = d && d.length || 0, b = b.substring(0, b.lastIndexOf("/")), h = function (a) {
                return a.replace(/(url\()['"]?([^\/\)'"][^:\)'"]+)['"]?(\))/g, "$1" + b + "$2$3")
            }, i = !g && c, j = 0, k, l, m, n, o;
            b.length && (b += "/"), i && (g = 1);
            for (; j < g; j++) {
                k = 0, i ? (l = c, f.push(h(a))) : (l = d[j].match(/@media ([^\{]+)\{([\S\s]+?)$/) && RegExp.$1, f.push(RegExp.$2 && h(RegExp.$2))), n = l.split(","), o = n.length;
                for (; k < o; k++)m = n[k], e.push({media: m.match(/(only\s+)?([a-zA-Z]+)(\sand)?/) && RegExp.$2, rules: f.length - 1, minw: m.match(/\(min\-width:[\s]*([\s]*[0-9]+)px[\s]*\)/) && parseFloat(RegExp.$1), maxw: m.match(/\(max\-width:[\s]*([\s]*[0-9]+)px[\s]*\)/) && parseFloat(RegExp.$1)})
            }
            r()
        }, p, q, r = function (a) {
            var b = "clientWidth", h = d[b], l = c.compatMode === "CSS1Compat" && h || c.body[b] || h, m = {}, n = c.createDocumentFragment(), o = k[k.length - 1], s = (new Date).getTime();
            if (a && p && s - p < i)clearTimeout(q), q = setTimeout(r, i); else {
                p = s;
                for (var t in e) {
                    var u = e[t];
                    if (!u.minw && !u.maxw || (!u.minw || u.minw && l >= u.minw) && (!u.maxw || u.maxw && l <= u.maxw))m[u.media] || (m[u.media] = []), m[u.media].push(f[u.rules])
                }
                for (var t in g)g[t] && g[t].parentNode === j && j.removeChild(g[t]);
                for (var t in m) {
                    var v = c.createElement("style"), w = m[t].join("\n");
                    v.type = "text/css", v.media = t, v.styleSheet ? v.styleSheet.cssText = w : v.appendChild(c.createTextNode(w)), n.appendChild(v), g.push(v)
                }
                j.insertBefore(n, o.nextSibling)
            }
        }, s = function (a, b) {
            var c = t();
            if (!!c) {
                c.open("GET", a, !0), c.onreadystatechange = function () {
                    c.readyState == 4 && (c.status == 200 || c.status == 304) && b(c.responseText)
                };
                if (c.readyState == 4)return;
                c.send()
            }
        }, t = function () {
            var a = !1, b = [function () {
                return new ActiveXObject("Microsoft.XMLHTTP")
            }, function () {
                return new XMLHttpRequest
            }], c = b.length;
            while (c--) {
                try {
                    a = b[c]()
                } catch (d) {
                    continue
                }
                break
            }
            return function () {
                return a
            }
        }();
        m(), respond.update = m, a.addEventListener ? a.addEventListener("resize", u, !1) : a.attachEvent && a.attachEvent("onresize", u)
    }
}(this, Modernizr.mq("only all")), function (a, b, c) {
    function k(a) {
        return!a || a == "loaded" || a == "complete"
    }

    function j() {
        var a = 1, b = -1;
        while (p.length - ++b)if (p[b].s && !(a = p[b].r))break;
        a && g()
    }

    function i(a) {
        var c = b.createElement("script"), d;
        c.src = a.s, c.onreadystatechange = c.onload = function () {
            !d && k(c.readyState) && (d = 1, j(), c.onload = c.onreadystatechange = null)
        }, m(function () {
            d || (d = 1, j())
        }, H.errorTimeout), a.e ? c.onload() : n.parentNode.insertBefore(c, n)
    }

    function h(a) {
        var c = b.createElement("link"), d;
        c.href = a.s, c.rel = "stylesheet", c.type = "text/css", !a.e && (w || r) ? function a(b) {
            m(function () {
                if (!d)try {
                    b.sheet.cssRules.length ? (d = 1, j()) : a(b)
                } catch (c) {
                    c.code == 1e3 || c.message == "security" || c.message == "denied" ? (d = 1, m(function () {
                        j()
                    }, 0)) : a(b)
                }
            }, 0)
        }(c) : (c.onload = function () {
            d || (d = 1, m(function () {
                j()
            }, 0))
        }, a.e && c.onload()), m(function () {
            d || (d = 1, j())
        }, H.errorTimeout), !a.e && n.parentNode.insertBefore(c, n)
    }

    function g() {
        var a = p.shift();
        q = 1, a ? a.t ? m(function () {
            a.t == "c" ? h(a) : i(a)
        }, 0) : (a(), j()) : q = 0
    }

    function f(a, c, d, e, f, h) {
        function i() {
            !o && k(l.readyState) && (r.r = o = 1, !q && j(), l.onload = l.onreadystatechange = null, m(function () {
                u.removeChild(l)
            }, 0))
        }

        var l = b.createElement(a), o = 0, r = {t: d, s: c, e: h};
        l.src = l.data = c, !s && (l.style.display = "none"), l.width = l.height = "0", a != "object" && (l.type = d), l.onload = l.onreadystatechange = i, a == "img" ? l.onerror = i : a == "script" && (l.onerror = function () {
            r.e = r.r = 1, g()
        }), p.splice(e, 0, r), u.insertBefore(l, s ? null : n), m(function () {
            o || (u.removeChild(l), r.r = r.e = o = 1, j())
        }, H.errorTimeout)
    }

    function e(a, b, c) {
        var d = b == "c" ? z : y;
        q = 0, b = b || "j", C(a) ? f(d, a, b, this.i++, l, c) : (p.splice(this.i++, 0, a), p.length == 1 && g());
        return this
    }

    function d() {
        var a = H;
        a.loader = {load: e, i: 0};
        return a
    }

    var l = b.documentElement, m = a.setTimeout, n = b.getElementsByTagName("script")[0], o = {}.toString, p = [], q = 0, r = "MozAppearance"in l.style, s = r && !!b.createRange().compareNode, t = r && !s, u = s ? l : n.parentNode, v = a.opera && o.call(a.opera) == "[object Opera]", w = "webkitAppearance"in l.style, x = w && "async"in b.createElement("script"), y = r ? "object" : v || x ? "img" : "script", z = w ? "img" : y, A = Array.isArray || function (a) {
        return o.call(a) == "[object Array]"
    }, B = function (a) {
        return typeof a == "object"
    }, C = function (a) {
        return typeof a == "string"
    }, D = function (a) {
        return o.call(a) == "[object Function]"
    }, E = [], F = {}, G, H;
    H = function (a) {
        function f(a) {
            var b = a.split("!"), c = E.length, d = b.pop(), e = b.length, f = {url: d, origUrl: d, prefixes: b}, g, h;
            for (h = 0; h < e; h++)g = F[b[h]], g && (f = g(f));
            for (h = 0; h < c; h++)f = E[h](f);
            return f
        }

        function e(a, b, e, g, h) {
            var i = f(a), j = i.autoCallback;
            if (!i.bypass) {
                b && (b = D(b) ? b : b[a] || b[g] || b[a.split("/").pop().split("?")[0]]);
                if (i.instead)return i.instead(a, b, e, g, h);
                e.load(i.url, i.forceCSS || !i.forceJS && /css$/.test(i.url) ? "c" : c, i.noexec), (D(b) || D(j)) && e.load(function () {
                    d(), b && b(i.origUrl, h, g), j && j(i.origUrl, h, g)
                })
            }
        }

        function b(a, b) {
            function c(a) {
                if (C(a))e(a, h, b, 0, d); else if (B(a))for (i in a)a.hasOwnProperty(i) && e(a[i], h, b, i, d)
            }

            var d = !!a.test, f = d ? a.yep : a.nope, g = a.load || a.both, h = a.callback, i;
            c(f), c(g), a.complete && b.load(a.complete)
        }

        var g, h, i = this.yepnope.loader;
        if (C(a))e(a, 0, i, 0); else if (A(a))for (g = 0; g < a.length; g++)h = a[g], C(h) ? e(h, 0, i, 0) : A(h) ? H(h) : B(h) && b(h, i); else B(a) && b(a, i)
    }, H.addPrefix = function (a, b) {
        F[a] = b
    }, H.addFilter = function (a) {
        E.push(a)
    }, H.errorTimeout = 1e4, b.readyState == null && b.addEventListener && (b.readyState = "loading", b.addEventListener("DOMContentLoaded", G = function () {
        b.removeEventListener("DOMContentLoaded", G, 0), b.readyState = "complete"
    }, 0)), a.yepnope = d()
}(this, this.document), Modernizr.load = function () {
    yepnope.apply(window, [].slice.call(arguments, 0))
};
/* main.js */
function getNav() {
    var mobileNav = $('nav[role=navigation] fieldset[role=site-search]').after('<fieldset role="mobile-nav"></fieldset>').next().append('<select></select>');
    mobileNav.children('select').append('<option value="">Navigate&hellip;</option>');
    $($('ul[role=main-navigation] a')).each(function (_, link) {
        mobileNav.children('select').append('<option value="' + link.href + '">&bull; ' + link.text + '</option>')
    });
    mobileNav.children('select').bind('change', function (event) {
        if (event.target.value) window.location.href = event.target.value;
    });
}
function addSidebarToggler() {
    $('#content').append('<span class="toggle-sidebar"></span>');
    $('.toggle-sidebar').bind('click', function (e) {
        e.preventDefault();
        if ($('body').hasClass('collapse-sidebar')) {
            $('body').removeClass('collapse-sidebar');
        } else {
            $('body').addClass('collapse-sidebar');
        }
    });
    sections = $('aside[role=sidebar] > section')
    if (sections.length > 1) {
        sections.each(function (index, section) {
            if ((sections.length >= 3) && index % 3 == 0) {
                $(section).addClass("first");
            }
            count = ((index + 1) % 2) ? "odd" : "even";
            $(section).addClass(count);
        });
    }
    if (sections.length >= 3) {
        $('aside[role=sidebar]').addClass('thirds')
    }
}
function testFeatures() {
    var features = ['maskImage'];
    $(features).map(function (_, feature) {
        if (Modernizr.testAllProps(feature)) {
            $('html').addClass(feature);
        } else {
            $('html').addClass('no-' + feature);
        }
    });
    if ("placeholder" in document.createElement("input")) {
        $('html').addClass('placeholder');
    } else {
        $('html').addClass('no-placeholder');
    }
}

function addCodeLineNumbers() {
    if (navigator.appName == 'Microsoft Internet Explorer') {
        return
    }
    $('div.gist-highlight').each(function (_, code) {
        var tableStart = '<table cellpadding="0" cellspacing="0"><tbody><tr><td class="gutter">';
        var lineNumbers = '<pre class="line-numbers">';
        var tableMiddle = '</pre></td><td class="code" width="100%">';
        var tableEnd = '</td></tr></tbody></table>';
        var count = $('div.line', code).length;
        for (i = 1; i <= count; i++) {
            lineNumbers += '<span class="line">' + i + '</span>\n';
        }
        table = tableStart + lineNumbers + tableMiddle + '<pre>' + $('pre', code).html() + '</pre>' + tableEnd;
        $(code).html(table);
    });
}

$(function () {
    testFeatures();
    addCodeLineNumbers();
    getNav();
    addSidebarToggler();
});

// iOS scaling bug fix
// Rewritten version
// By @mathias, @cheeaun and @jdalton
// Source url: https://gist.github.com/901295
(function (doc) {
    var addEvent = 'addEventListener',
        type = 'gesturestart',
        qsa = 'querySelectorAll',
        scales = [1, 1],
        meta = qsa in doc ? doc[qsa]('meta[name=viewport]') : [];

    function fix() {
        meta.content = 'width=device-width,minimum-scale=' + scales[0] + ',maximum-scale=' + scales[1];
        doc.removeEventListener(type, fix, true);
    }

    if ((meta = meta[meta.length - 1]) && addEvent in doc) {
        fix();
        scales = [.25, 1.6];
        doc[addEvent](type, fix, true);
    }
}(document));

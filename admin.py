# -*- coding: utf-8 -*-
import StringIO
from hashlib import md5
from time import time

from PIL import Image
from tornado import escape
import sae.storage

from common import BaseHandler, authorized, safe_encode, clear_cache_by_pathlist, quoted_string, clear_all_cache, genArchive, setAttr, clearAllKVDB, set_count, increment, getAttr
from helpers import generate_random
from setting import *
from extensions.imagelib import Recaptcha
from model import Article, Comment, Link, Category, Tag, User, MyData, Archive


try:
    import json
except:
    import simplejson as json

if not debug:
    import sae.mail
    from sae.taskqueue import add_task


def put_saestorage(file_name='', data='', expires='365', type=None, encoding=None, domain_name=STORAGE_DOMAIN_NAME):
    s = sae.storage.Client()
    ob = sae.storage.Object(data=data, cache_control='access plus %s day' % expires, content_type=type,
                            content_encoding=encoding)
    #return s.put(domain_name, str(datetime.now().strftime("%Y%m") + "/" + file_name), ob)
    return s.put(domain_name, file_name, ob)


def get_saestorage(domain_name=STORAGE_DOMAIN_NAME):
    s = sae.storage.Client()
    filelist = s.list(domain_name)
    total_count = filelist
    return filelist


class HomePage(BaseHandler):
    @authorized()
    def get(self):
        output = self.render('admin_index.html', {
            'title': "后台首页",
            'keywords': getAttr('KEYWORDS'),
            'description': getAttr('SITE_DECR'),
            'test': '',
        }, layout='_layout_admin.html')
        self.write(output)
        return output


class Login(BaseHandler):
    def get(self):
        self.echo('admin_login.html')

    def post(self):
        try:
            name = self.get_argument("name")
            password = self.get_argument("password")
            captcha = self.get_argument("captcha")
        except:
            self.redirect('%s/admin/login' % BASE_URL)
            return
        if self.get_secure_cookie("captcha") != captcha:
            self.redirect('%s/admin/' % BASE_URL)
            return

        if name and password:
            has_user = User.check_has_user()
            if has_user:
                password = md5(password.encode('utf-8')).hexdigest()
                user = User.check_user(name, password)
                if user:
                    self.set_secure_cookie('username', name, expires_days=365)
                    self.set_secure_cookie('userpw', password, expires_days=365)
                    self.redirect('%s/admin/' % BASE_URL)
                    return
                else:
                    self.redirect('%s/admin/login' % BASE_URL)
                    return
            else:
                # add new user
                newuser = User.add_user(name, password)
                if newuser:
                    self.set_secure_cookie('username', name, expires_days=365)
                    self.set_secure_cookie('userpw', md5(password.encode('utf-8')).hexdigest(), expires_days=365)
                    self.redirect('%s/admin/' % BASE_URL)
                    return
                else:
                    self.redirect('%s/admin/login' % BASE_URL)
                    return
        else:
            self.redirect('%s/admin/login' % BASE_URL)


class Logout(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect('%s/admin/login' % BASE_URL)


class AddUser(BaseHandler):
    @authorized()
    def get(self):
        pass


class Forbidden(BaseHandler):
    def get(self):
        self.write('Forbidden page')


class FileUpload(BaseHandler):
    @authorized()
    def post(self):
        self.set_header('Content-Type', 'text/html')
        rspd = {'status': 201, 'msg': 'ok'}
        max_size = 10240000 # 10MB
        fileupload = self.request.files['imgFile']
        if fileupload:
            myfile = fileupload[0]
            if not myfile['filename']:
                self.write(json.dumps(
                    {'error': 1, 'message': u'请选择要上传的文件'}
                ))
                return

            # if myfile.size > max_size:
            #     self.write(json.dumps(
            #         { 'error': 1, 'message': u'上传的文件大小不能超过2.5MB'}
            #     ))
            #     return

            try:
                file_type = myfile['filename'].split('.')[-1].lower()
                new_file_name = "%s.%s" % (str(int(time())), file_type)
                # 缩放图片
                if file_type in ['jpg', 'jpeg', 'png', 'gif']:
                    im = Image.open(StringIO.StringIO(myfile['body']))
                    im.show()
                    width, height = im.size
                    if width > 750:
                        ratio = 1.0 * height / width
                        new_height = int(750 * ratio)
                        new_size = (750, new_height)
                        out = im.resize(new_size, Image.ANTIALIAS)
                        print "Before"
                        myfile['body'] = out.toString('jpeg', 'RGB')
                        file_type = 'jpg'
                        print 750, new_height
                        new_file_name = "%s-thumb.%s" % (str(int(time())), file_type)
                    else:
                        pass
                else:
                    pass
            except:
                file_type = ''
                new_file_name = str(int(time()))
                ##
            mime_type = myfile['content_type']
            encoding = None
            ###

            try:
                attachment_url = put_saestorage(file_name=new_file_name, data=myfile['body'], expires='365',
                                                type=mime_type, encoding=encoding)
            except:
                attachment_url = ''

            if attachment_url:
                rspd['status'] = 200
                rspd['error'] = 0
                rspd['filename'] = myfile['filename']
                rspd['url'] = attachment_url
            else:
                rspd['status'] = 500
                rspd['error'] = 1
                rspd['message'] = 'put_saestorage error, try it again.'
        else:
            rspd['message'] = 'No file uploaded'
        self.write(json.dumps(rspd))
        return


class FileManager(BaseHandler):
    @authorized()
    def get(self):
        self.set_header('Content-Type', 'text/html')
        rspd = {'moveup_dir_path': '/', 'current_dir_path': '/'}
        file_list = get_saestorage()
        rspd['current_url'] = '/'
        rspd['total_count'] = len(file_list)
        rspd['file_list'] = file_list
        self.write(json.dumps(rspd))
        return


class AddPost(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_post_add.html', {
            'title': "添加文章",
            'method': "/admin/add_post",
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_all_tag_name(),
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        self.set_header('Content-Type', 'application/json')
        rspd = {'status': 201, 'msg': 'ok'}

        try:
            tf = {'true': 1, 'false': 0}
            timestamp = int(time())
            post_dic = {
                'category': self.get_argument("cat"),
                'title': self.get_argument("tit"),
                'content': self.get_argument("con"),
                'tags': self.get_argument("tag", '').replace(u'，', ','),
                'closecomment': self.get_argument("clo", '0'),
                'password': self.get_argument("password", ''),
                'add_time': timestamp,
                'edit_time': timestamp,
                'archive': genArchive(),
            }
            if post_dic['tags']:
                tagslist = set([x.strip() for x in post_dic['tags'].split(',')])
                try:
                    tagslist.remove('')
                except:
                    pass
                if tagslist:
                    post_dic['tags'] = ','.join(tagslist)
            post_dic['closecomment'] = tf[post_dic['closecomment'].lower()]
        except:
            rspd['status'] = 500
            rspd['msg'] = '错误： 注意必填的三项'
            self.write(json.dumps(rspd))
            return

        postid = Article.add_new_article(post_dic)
        if postid:
            keyname = 'pv_%s' % (str(postid))
            set_count(keyname, 0, 0)

            Category.add_postid_to_cat(post_dic['category'], str(postid))
            Archive.add_postid_to_archive(genArchive(), str(postid))
            increment('Totalblog')

            if post_dic['tags']:
                Tag.add_postid_to_tags(post_dic['tags'].split(','), str(postid))

            rspd['status'] = 200
            rspd['msg'] = '完成： 你已经成功添加了一篇文章 <a href="/t/%s" target="_blank">查看</a>' % str(postid)
            rspd['postid'] = postid
            rspd['method'] = "/admin/edit_post"
            clear_cache_by_pathlist(['/', 'cat:%s' % quoted_string(post_dic['category'])])

            if not debug:
                add_task('default', '/task/pingrpctask')

            self.write(json.dumps(rspd))
            return
        else:
            rspd['status'] = 500
            rspd['msg'] = '错误： 未知错误，请尝试重新提交'
            self.write(json.dumps(rspd))
            return


class ListPost(BaseHandler):
    @authorized()
    def get(self, direction='next', page='2', base_id='1'):
        self.echo('admin_post_list.html', {
            'title': "文章列表",
            'objs': Article.get_all_article(),
            # TODO 后台文章管理要分页
            # 'objs': Article.get_page_posts(direction, page, base_id, 20),
        }, layout='_layout_admin.html')


class EditPost(BaseHandler):
    @authorized()
    def get(self, id=''):
        obj = None
        if id:
            obj = Article.get_article_by_id_edit(id)
        self.echo('admin_post_edit.html', {
            'title': "编辑文章",
            'method': "/admin/edit_post/" + id,
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_all_tag_name(),
            'obj': obj
        }, layout='_layout_admin.html')

    @authorized()
    def post(self, id=''):
        act = self.get_argument("act", '')
        if act == 'findid':
            eid = self.get_argument("id", '')
            self.redirect('%s/admin/edit_post/%s' % (BASE_URL, eid))
            return

        self.set_header('Content-Type', 'application/json')
        rspd = {'status': 201, 'msg': 'ok'}
        oldobj = Article.get_article_by_id_edit(id)

        try:
            tf = {'true': 1, 'false': 0}
            timestamp = int(time())
            post_dic = {
                'category': self.get_argument("cat"),
                'title': self.get_argument("tit"),
                'content': self.get_argument("con"),
                'tags': self.get_argument("tag", '').replace(u'，', ','),
                'closecomment': self.get_argument("clo", 'false'),
                'password': self.get_argument("password", ''),
                'edit_time': timestamp,
                'id': id
            }

            if post_dic['tags']:
                tagslist = set([x.strip() for x in post_dic['tags'].split(',')])
                try:
                    tagslist.remove('')
                except:
                    pass
                if tagslist:
                    post_dic['tags'] = ','.join(tagslist)
            post_dic['closecomment'] = tf[post_dic['closecomment'].lower()]
        except:
            rspd['status'] = 500
            rspd['msg'] = '错误： 注意必填的三项'
            self.write(json.dumps(rspd))
            return

        postid = Article.update_post_edit(post_dic)
        if postid:
            cache_key_list = ['/', 'post:%s' % id, 'cat:%s' % quoted_string(oldobj.category)]
            if oldobj.category != post_dic['category']:
                #cat changed 
                Category.add_postid_to_cat(post_dic['category'], str(postid))
                Category.remove_postid_from_cat(oldobj.category, str(postid))
                cache_key_list.append('cat:%s' % quoted_string(post_dic['category']))

            if oldobj.tags != post_dic['tags']:
                #tag changed 
                old_tags = set(oldobj.tags.split(','))
                new_tags = set(post_dic['tags'].split(','))

                removed_tags = old_tags - new_tags
                added_tags = new_tags - old_tags

                if added_tags:
                    Tag.add_postid_to_tags(added_tags, str(postid))

                if removed_tags:
                    Tag.remove_postid_from_tags(removed_tags, str(postid))

            clear_cache_by_pathlist(cache_key_list)
            rspd['status'] = 200
            rspd['msg'] = '完成： 你已经成功编辑了一篇文章 <a href="/t/%s" target="_blank">查看编辑后的文章</a>' % str(postid)
            self.write(json.dumps(rspd))
            return
        else:
            rspd['status'] = 500
            rspd['msg'] = '错误： 未知错误，请尝试重新提交'
            self.write(json.dumps(rspd))
            return


class DelPost(BaseHandler):
    @authorized()
    def get(self, id=''):
        try:
            if id:
                oldobj = Article.get_article_by_id_edit(id)
                Category.remove_postid_from_cat(oldobj.category, str(id))
                Archive.remove_postid_from_archive(oldobj.archive, str(id))
                Tag.remove_postid_from_tags(set(oldobj.tags.split(',')), str(id))
                Article.del_post_by_id(id)
                increment('Totalblog', NUM_SHARDS, -1)
                cache_key_list = ['/', 'post:%s' % id, 'cat:%s' % quoted_string(oldobj.category)]
                clear_cache_by_pathlist(cache_key_list)
                clear_cache_by_pathlist(['post:%s' % id])
                self.redirect('%s/admin/list_post' % (BASE_URL))
        except:
            pass


class EditComment(BaseHandler):
    @authorized()
    def get(self, id=''):
        obj = None
        if id:
            obj = Comment.get_comment_by_id(id)
            if obj:
                act = self.get_argument("act", '')
                if act == 'del':
                    Comment.del_comment_by_id(id)
                    clear_cache_by_pathlist(['post:%d' % obj.postid])
                    self.redirect('%s/admin/comment/' % (BASE_URL))
                    return
        self.echo('admin_comment.html', {
            'title': "评论管理",
            'cats': Category.get_all_cat_name(),
            'tags': Tag.get_all_tag_name(),
            'obj': obj,
            'comments': Comment.get_recent_comments(ADMIN_RECENT_COMMENT_NUM),
        }, layout='_layout_admin.html')

    @authorized()
    def post(self, id=''):
        act = self.get_argument("act", '')
        if act == 'findid':
            eid = self.get_argument("id", '')
            self.redirect('%s/admin/comment/%s' % (BASE_URL, eid))
            return

        tf = {'true': 1, 'false': 0}
        post_dic = {
            'author': self.get_argument("author"),
            'email': self.get_argument("email", ''),
            'content': safe_encode(self.get_argument("content").replace('\r', '\n')),
            'url': self.get_argument("url", ''),
            'visible': self.get_argument("visible", 'false'),
            'id': id
        }
        post_dic['visible'] = tf[post_dic['visible'].lower()]

        Comment.update_comment_edit(post_dic)
        clear_cache_by_pathlist(['post:%s' % id])
        self.redirect('%s/admin/comment/%s' % (BASE_URL, id))
        return


class LinkBroll(BaseHandler):
    @authorized()
    def get(self):
        act = self.get_argument("act", '')
        id = self.get_argument("id", '')

        obj = None
        if act == 'del':
            if id:
                Link.del_link_by_id(id)
                clear_cache_by_pathlist(['/'])
            self.redirect('%s/admin/links' % BASE_URL)
            return
        elif act == 'edit':
            if id:
                obj = Link.get_link_by_id(id)
                clear_cache_by_pathlist(['/'])
        self.echo('admin_link.html', {
            'title': "友情链接",
            'objs': Link.get_all_links(),
            'obj': obj,
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        act = self.get_argument("act", '')
        id = self.get_argument("id", '')
        name = self.get_argument("name", '')
        sort = self.get_argument("sort", '0')
        url = self.get_argument("url", '')

        if name and url:
            params = {'id': id, 'name': name, 'url': url, 'displayorder': sort}
            if act == 'add':
                Link.add_new_link(params)

            if act == 'edit':
                Link.update_link_edit(params)

            clear_cache_by_pathlist(['/'])

        self.redirect('%s/admin/links' % BASE_URL)
        return


class BlogSetting(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_setting.html', {
            'title': "站点信息",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        value = self.get_argument("SITE_TITLE", '')
        if value:
            setAttr('SITE_TITLE', value)
        value = self.get_argument("SITE_TITLE2", '')
        if value:
            setAttr('SITE_TITLE2', value)

        value = self.get_argument("SITE_SUB_TITLE", '')
        if value:
            setAttr('SITE_SUB_TITLE', value)

        value = self.get_argument("KEYWORDS", '')
        if value:
            setAttr('KEYWORDS', value)

        value = self.get_argument("SITE_DECR", '')
        if value:
            setAttr('SITE_DECR', value)

        value = self.get_argument("ADMIN_NAME", '')
        if value:
            setAttr('ADMIN_NAME', value)

        value = self.get_argument("MOVE_SECRET", '')
        if value:
            setAttr('MOVE_SECRET', value)

        value = self.get_argument("NOTICE_MAIL", '')
        if value:
            setAttr('NOTICE_MAIL', value)

        clear_cache_by_pathlist(['/'])

        self.redirect('%s/admin/setting' % BASE_URL)
        return


class BlogSetting2(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_setting2.html', {
            'title': "邮箱配置",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        value = self.get_argument("MAIL_FROM", '')
        if value:
            setAttr('MAIL_FROM', value)

        value = self.get_argument("MAIL_KEY", '')
        if value:
            setAttr('MAIL_KEY', value)

        value = self.get_argument("MAIL_SMTP", '')
        if value:
            setAttr('MAIL_SMTP', value)

        value = self.get_argument("MAIL_PORT", '')
        if value:
            setAttr('MAIL_PORT', value)

        clear_cache_by_pathlist(['/'])

        self.redirect('%s/admin/setting2' % BASE_URL)
        return


class BlogSetting3(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_setting3.html', {
            'title': "详细参数",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        EACH_PAGE_POST_NUM = self.get_argument("EACH_PAGE_POST_NUM", '')
        if EACH_PAGE_POST_NUM:
            setAttr('EACH_PAGE_POST_NUM', EACH_PAGE_POST_NUM)

        EACH_PAGE_COMMENT_NUM = self.get_argument("EACH_PAGE_COMMENT_NUM", '')
        if EACH_PAGE_COMMENT_NUM:
            setAttr('EACH_PAGE_COMMENT_NUM', EACH_PAGE_COMMENT_NUM)

        RELATIVE_POST_NUM = self.get_argument("RELATIVE_POST_NUM", '')
        if RELATIVE_POST_NUM:
            setAttr('RELATIVE_POST_NUM', RELATIVE_POST_NUM)

        SHORTEN_CONTENT_WORDS = self.get_argument("SHORTEN_CONTENT_WORDS", '')
        if SHORTEN_CONTENT_WORDS:
            setAttr('SHORTEN_CONTENT_WORDS', SHORTEN_CONTENT_WORDS)

        DESCRIPTION_CUT_WORDS = self.get_argument("DESCRIPTION_CUT_WORDS", '')
        if DESCRIPTION_CUT_WORDS:
            setAttr('DESCRIPTION_CUT_WORDS', DESCRIPTION_CUT_WORDS)

        EACH_PAGE_COMMENT_NUM = self.get_argument("EACH_PAGE_COMMENT_NUM", '')
        if EACH_PAGE_COMMENT_NUM:
            setAttr('EACH_PAGE_COMMENT_NUM', EACH_PAGE_COMMENT_NUM)

        RECENT_COMMENT_CUT_WORDS = self.get_argument("RECENT_COMMENT_CUT_WORDS", '')
        if RECENT_COMMENT_CUT_WORDS:
            setAttr('RECENT_COMMENT_CUT_WORDS', RECENT_COMMENT_CUT_WORDS)

        LINK_NUM = self.get_argument("LINK_NUM", '')
        if LINK_NUM:
            setAttr('LINK_NUM', LINK_NUM)

        MAX_COMMENT_NUM_A_DAY = self.get_argument("MAX_COMMENT_NUM_A_DAY", '')
        if MAX_COMMENT_NUM_A_DAY:
            setAttr('MAX_COMMENT_NUM_A_DAY', MAX_COMMENT_NUM_A_DAY)

        COMMENT_DEFAULT_VISIBLE = self.get_argument("COMMENT_DEFAULT_VISIBLE", '')
        if COMMENT_DEFAULT_VISIBLE:
            setAttr('COMMENT_DEFAULT_VISIBLE', COMMENT_DEFAULT_VISIBLE)

        PAGE_CACHE_TIME = self.get_argument("PAGE_CACHE_TIME", '')
        if PAGE_CACHE_TIME:
            setAttr('PAGE_CACHE_TIME', PAGE_CACHE_TIME)

        POST_CACHE_TIME = self.get_argument("POST_CACHE_TIME", '')
        if POST_CACHE_TIME:
            setAttr('POST_CACHE_TIME', POST_CACHE_TIME)

        HOT_TAGS_NUM = self.get_argument("HOT_TAGS_NUM", '')
        if HOT_TAGS_NUM:
            setAttr('HOT_TAGS_NUM', HOT_TAGS_NUM)

        MAX_ARCHIVES_NUM = self.get_argument("MAX_ARCHIVES_NUM", '')
        if MAX_ARCHIVES_NUM:
            setAttr('MAX_ARCHIVES_NUM', MAX_ARCHIVES_NUM)

        clear_cache_by_pathlist(['/'])

        self.redirect('%s/admin/setting3' % BASE_URL)
        return


class BlogSetting4(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_setting4.html', {
            'title': "广告统计",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        ANALYTICS_CODE = self.get_argument("ANALYTICS_CODE", '')
        if ANALYTICS_CODE:
            setAttr('ANALYTICS_CODE', ANALYTICS_CODE)

        ADSENSE_CODE1 = self.get_argument("ADSENSE_CODE1", '')
        if ADSENSE_CODE1:
            setAttr('ADSENSE_CODE1', ADSENSE_CODE1)

        ADSENSE_CODE2 = self.get_argument("ADSENSE_CODE2", '')
        if ADSENSE_CODE2:
            setAttr('ADSENSE_CODE2', ADSENSE_CODE2)

        clear_cache_by_pathlist(['/'])

        self.redirect('%s/admin/setting4' % BASE_URL)
        return


class EditProfile(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_profile.html', {
            'title': "个人资料",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        oldPassword = self.get_argument("oldPassword", '')
        newPassword = self.get_argument("newPassword", '')
        newPassword2 = self.get_argument("newPassword2", '')
        if oldPassword and newPassword and newPassword2:
            if newPassword == newPassword2:
                username = self.get_secure_cookie('username')
                oldPassword = md5(oldPassword.encode('utf-8')).hexdigest()
                user = User.check_user(username, oldPassword)
                if user:
                    User.update_user(username, newPassword)
                    self.set_secure_cookie('userpw', '123', expires_days=1)
                    self.write(escape.json_encode(1))
                    return
                else:
                    pass
            else:
                pass
        else:
            pass
        self.write(escape.json_encode(0))


# TODO KVDB 管理
class KVDBAdmin(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_kvdb.html', {
            'title': "KVDB 管理",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        self.redirect('%s/admin/kvdb' % BASE_URL)
        return


class FlushData(BaseHandler):
    @authorized()
    def get(self):
        self.echo('admin_flushdata.html', {
            'title': "缓存管理",
        }, layout='_layout_admin.html')

    @authorized()
    def post(self):
        act = self.get_argument("act", '')
        if act == 'flush':
            MyData.flush_all_data()
            clear_all_cache()
            clearAllKVDB()
            print 'flush'
            self.redirect('/admin/flushdata')
            return
        elif act == 'flushcache':
            clear_all_cache()
            print 'flushcache'
            self.redirect('/admin/flushdata')
            return


class PingRPCTask(BaseHandler):
    def get(self):
        for n in range(len(XML_RPC_ENDPOINTS)):
            add_task('default', '%s/task/pingrpc/%d' % (BASE_URL, n))
        self.write(str(time()))

    post = get


class PingRPC(BaseHandler):
    def get(self, n=0):
        import urllib2

        pingstr = self.render('rpc.xml', {'article_id': Article.get_max_id()})

        headers = {
            'User-Agent': 'request',
            'Content-Type': 'text/xml',
            'Content-length': str(len(pingstr))
        }

        req = urllib2.Request(
            url=XML_RPC_ENDPOINTS[int(n)],
            headers=headers,
            data=pingstr,
        )
        try:
            content = urllib2.urlopen(req).read()
            tip = 'Ping ok' + content
        except:
            tip = 'ping erro'

        self.write(str(time()) + ": " + tip)
        #add_task('default', '%s/task/sendmail'%BASE_URL, urlencode({'subject': tip, 'content': tip + " " + str(n)}))

    post = get


class SendMail(BaseHandler):
    def post(self):
        subject = self.get_argument("subject", '')
        content = self.get_argument("content", '')

        if subject and content:
            sae.mail.send_mail(getAttr('NOTICE_MAIL'), subject, content,
                               (getAttr('MAIL_SMTP'), int(getAttr('MAIL_PORT')), getAttr('MAIL_FROM'),
                                getAttr('MAIL_KEY'), True))


# 初始化一些参数
def Init():
    if not getAttr('SITE_TITLE'):
        setAttr('SITE_TITLE', SITE_TITLE)
    if not getAttr('SITE_TITLE2'):
        setAttr('SITE_TITLE2', SITE_TITLE2)
    if not getAttr('SITE_SUB_TITLE'):
        setAttr('SITE_SUB_TITLE', SITE_SUB_TITLE)
    if not getAttr('KEYWORDS'):
        setAttr('KEYWORDS', KEYWORDS)
    if not getAttr('SITE_DECR'):
        setAttr('SITE_DECR', SITE_DECR)
    if not getAttr('ADMIN_NAME'):
        setAttr('ADMIN_NAME', ADMIN_NAME)
    if not getAttr('NOTICE_MAIL'):
        setAttr('NOTICE_MAIL', NOTICE_MAIL)
    if not getAttr('MOVE_SECRET'):
        setAttr('MOVE_SECRET', MOVE_SECRET)

    if not getAttr('MAIL_FROM'):
        setAttr('MAIL_FROM', MAIL_FROM)
    if not getAttr('MAIL_SMTP'):
        setAttr('MAIL_SMTP', MAIL_SMTP)
    if not getAttr('MAIL_PORT'):
        setAttr('MAIL_PORT', MAIL_PORT)
    if not getAttr('MAIL_KEY'):
        setAttr('MAIL_KEY', MAIL_KEY)

    if not getAttr('EACH_PAGE_POST_NUM'):
        setAttr('EACH_PAGE_POST_NUM', EACH_PAGE_POST_NUM)
    if not getAttr('EACH_PAGE_COMMENT_NUM'):
        setAttr('EACH_PAGE_COMMENT_NUM', EACH_PAGE_COMMENT_NUM)
    if not getAttr('RELATIVE_POST_NUM'):
        setAttr('RELATIVE_POST_NUM', RELATIVE_POST_NUM)
    if not getAttr('SHORTEN_CONTENT_WORDS'):
        setAttr('SHORTEN_CONTENT_WORDS', SHORTEN_CONTENT_WORDS)
    if not getAttr('DESCRIPTION_CUT_WORDS'):
        setAttr('DESCRIPTION_CUT_WORDS', DESCRIPTION_CUT_WORDS)
    if not getAttr('RECENT_COMMENT_NUM'):
        setAttr('RECENT_COMMENT_NUM', RECENT_COMMENT_NUM)
    if not getAttr('RECENT_COMMENT_CUT_WORDS'):
        setAttr('RECENT_COMMENT_CUT_WORDS', RECENT_COMMENT_CUT_WORDS)
    if not getAttr('LINK_NUM'):
        setAttr('LINK_NUM', LINK_NUM)
    if not getAttr('MAX_COMMENT_NUM_A_DAY'):
        setAttr('MAX_COMMENT_NUM_A_DAY', MAX_COMMENT_NUM_A_DAY)
    if not getAttr('PAGE_CACHE_TIME'):
        setAttr('PAGE_CACHE_TIME', PAGE_CACHE_TIME)
    if not getAttr('POST_CACHE_TIME'):
        setAttr('POST_CACHE_TIME', POST_CACHE_TIME)
    if not getAttr('HOT_TAGS_NUM'):
        setAttr('HOT_TAGS_NUM', HOT_TAGS_NUM)
    if not getAttr('MAX_ARCHIVES_NUM'):
        setAttr('MAX_ARCHIVES_NUM', MAX_ARCHIVES_NUM)
    if not getAttr('COMMENT_DEFAULT_VISIBLE'):
        setAttr('COMMENT_DEFAULT_VISIBLE', COMMENT_DEFAULT_VISIBLE)

    if not getAttr('ANALYTICS_CODE'):
        setAttr('ANALYTICS_CODE', ANALYTICS_CODE)
    if not getAttr('ADSENSE_CODE1'):
        setAttr('ADSENSE_CODE1', ADSENSE_CODE1)
    if not getAttr('ADSENSE_CODE2'):
        setAttr('ADSENSE_CODE2', ADSENSE_CODE2)


class Install(BaseHandler):
    def get(self):
        try:
            self.write('如果出现错误请尝试刷新本页。')
            has_user = User.check_has_user()
            if has_user:
                self.write('博客已经成功安装了，你可以直接 <a href="/admin/flushdata">清空网站数据</a>')
            else:
                self.write('博客数据库已经建立，现在就去 <a href="/admin/">设置一个管理员帐号</a>')
        except:
            try:
                MyData.creat_table()
                Init()  # 初始化系统参数
            except:
                pass
            self.write('博客已经成功安装了，现在就去 <a href="/admin/">设置一个管理员帐号</a>')


class GetCaptcha(BaseHandler):
    def get(self):
        text = generate_random(4)
        self.set_secure_cookie("captcha", text)

        strIO = Recaptcha(text)

        # ,mimetype='image/png'
        self.set_header("Content-Type", "image/png")
        self.write(strIO.read())
        return


class NotFoundPage(BaseHandler):
    def get(self):
        self.set_status(404)
        self.echo('error.html', {
            'page': '404',
            'title': "Can't find out this URL",
            'h2': 'Oh, my god!',
            'msg': '<script type="text/javascript" src="http://www.qq.com/404/search_children.js?edition=small" charset="utf-8"></script>'
        })

#####
urls = [
    (r"/admin/", HomePage),
    (r"/admin/login", Login),
    (r"/admin/logout", Logout),
    (r"/admin/403", Forbidden),
    (r"/admin/add_post", AddPost),
    (r"/admin/edit_post/(\d*)", EditPost),
    (r"/admin/list_post", ListPost),  # TODO 分页
    (r"/admin/del_post/(\d+)", DelPost),
    (r"/admin/comment/(\d*)", EditComment),
    (r"/admin/flushdata", FlushData),
    (r"/task/pingrpctask", PingRPCTask),
    (r"/task/pingrpc/(\d+)", PingRPC),
    (r"/task/sendmail", SendMail),
    (r"/install/125004628", Install),
    (r"/admin/fileupload", FileUpload),
    (r"/admin/filelist", FileManager),
    (r"/admin/links", LinkBroll),
    (r"/captcha/", GetCaptcha),
    (r"/admin/setting", BlogSetting),
    (r"/admin/setting2", BlogSetting2),
    (r"/admin/setting3", BlogSetting3),
    (r"/admin/setting4", BlogSetting4),
    (r"/admin/profile", EditProfile),
    (r"/admin/kvdb", KVDBAdmin),
    (r".*", NotFoundPage)
]
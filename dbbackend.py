# coding: utf8
import os
import sys
import pymongo
import config

DEBUG = config.DEBUG


class BaseManager(object):

    def __init__(self, collect):
        self.collect = collect

    def _response(self, data=None, error=None):
        return {"data": data, "error": error}

    def find(self, query=None):
        try:
            query = query or {}

            data = [d for d in self.collect.find(query)]
            response = self._response(data)
        except Exception, e:
            response = self._response(error=e)
        return response

    def count(self, query=None):
        query = query or {}
        try:
            response = self._response(self.collect.find(query).count())
        except Exception:
            response = self._response(error="Operatiion error...")
        return response

    def find_ext(self, limit, skip):
        try:
            cur = self.collect.find().sort("_id", direction=-1).skip(skip).\
                limit(limit)
            response = self._response([d for d in cur])
        except Exception, e:
            self.print_debug_info(str(e))
            response = self._response(error="Find error...")
        return response

    def update(self, id, set):
        response = self._response()
        try:
            self.collect.update({"_id": ObjectId(id), "$set": set},
                                upsert=False)
            response["data"] = True
        except Exception:
            response["error"] = "Update {} error...".format(self.collect)

        return response

    def update_by_permalink(self, permalink, set):
        response = self._response()
        try:
            self.collect.update({"permalink": permalink}, {"$set": set},
                                upsert=False)
            response["data"] = True
        except Exception:
            response["error"] = "Update {} error...".format(self.collect)

        return response

    def insert(self, set):
        response = self._response()
        try:
            response["data"] = self.collect.insert(set)
        except Exception, e:
            self.print_debug_info(str(e))
            response["error"] = "Update {} error...".format(self.collect)
        return response

    def find_by_permalink(self, permalink):
        response = self._response()
        try:
            cur = self.collect.find_one({'permalink': permalink})
            response["data"] = cur
        except Exception:
            response["error"] = "Error find one..."
        return response

    def find_by_id(self, id):
        try:
            cur = self.collect.find_one({'_id': ObjectId(id)})
            response = self._response(cur)
        except Exception:
            response = self._response(error='Post not found..')
        return response

    def get_paginator(self, limit, skip, tag=None, search=None,
                       search_fields=None):
        response = self._response()
        cond = {}
        if tag is not None:
            cond = {'tags': tag}
        elif search and search_fields:
            cond = {'$or': []}
            add = {'$regex': search, '$options': 'i'}
            for sf in search_fields:
                cond["$or"].append({sf:add})
        try:
            cur = self.collect.find(cond).skip(skip).limit(limit)
            response['data'] = [r for r in cur]
        except Exception, e:
            self.print_debug_info(e, DEBUG)
            response['error'] = 'Data not found...'
        return response

    @staticmethod
    def print_debug_info(msg, show=DEBUG):
        if show:
            error_color = '\033[32m'
            error_end = '\033[0m'

            error = {'type': sys.exc_info()[0].__name__,
                     'file': os.path.basename(
                sys.exc_info()[2].tb_frame.f_code.co_filename),
                'line': sys.exc_info()[2].tb_lineno,
                'details': str(msg)}

            print error_color
            print '\n\n---\nError type: %s in file: %s on line: %s\nError details: %s\n---\n\n'\
                  % (error['type'], error['file'], error['line'],
                     error['details'])
            print error_end


class User(BaseManager):

    def __init__(self, collect):
        super(User, self).__init__(collect)

    def get_users(self, limit, skip, tag=None, search=None, search_fields=None):
        search_fields = search_fields or ["name", "l_name"]
        return self.get_paginator(limit, skip, tag, search, search_fields)


class News(BaseManager):

    def __init__(self, collect):
        super(News, self).__init__(collect)

    def get_news(self, limit, skip, tag=None, search=None, search_fields=None):
        search_fields = search_fields or ["title", "body", "time"]
        return self.get_paginator(limit, skip, tag, search, search_fields)

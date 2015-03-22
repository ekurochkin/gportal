# coding: utf8
import os
import sys
import pymongo

DEBUG = True

class BaseManager:

    def __init__(self, collect):
        self.collect = collect

    def _responce(self, data=None, error=None):
        return {"data": data, "error": error}

    def find(self, query=None):
        try:
            if not query:
                query = {}

            data = [d for d in self.collect.find(query)]
            responce = self._responce(data)
        except Exception, e:
            responce = self._responce(error=e)
        return responce

    def count(self, query=None):
        try:
            responce = self._responce(self.collect.find(query).count())
        except Exception:
            responce = self._responce(error="Operatiion error...")
        return responce

    def find_ext(self, limit, skip):
        try:
            cur = self.collect.find().sort("_id", direction=-1).skip(skip).\
                limit(limit)
            responce = self._responce([d for d in cur])
        except Exception, e:
            self.print_debug_info(str(e))
            responce = self._responce(error="Find error...")
        return responce

    def update(self, id, set):
        try:
            self.collect.update({"_id": ObjectId(id), "$set": set},
                                upsert=False)
            self.responce["data"] = True
        except Exception:
            self.responce["error"] = "Update {} error...".format(self.collect)

        return self.responce

    def insert(self, set):
        try:
            self.responce["data"] = self.collect.insert(set)
        except Exception, e:
            self.print_debug_info(str(e))
            self.responce["error"] = "Update {} error...".format(self.collect)
        return self.responce

    def find_by_permalink(self, permalink):
        try:
            cur = self.collect.find_one({'permalink': permalink})
            return cur
        except Exception:
            return "Error find one..."

    def find_by_id(self, id):
        try:
            cur = self.collect.find_one({'_id': ObjectId(id)})
            responce = self._responce(cur)
        except Exception:
            responce = self._response(error='Post not found..')
        return responce

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


class User(object):
    def __init__(self, collect):
        super(User, self).__init__(collect)        
		       
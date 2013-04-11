class Li(object):

    def pop(self):
        print "pop()"

li = Li()
p = getattr(li, "pop")()
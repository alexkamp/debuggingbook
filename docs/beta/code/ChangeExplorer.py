#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "The Debugging Book".
# Web site: https://www.debuggingbook.org/html/ChangeExplorer.html
# Last change: 2021-01-10 13:21:53+01:00
#
#!/
# Copyright (c) 2018-2021 CISPA, Saarland University, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# # Where the Bugs are

if __name__ == "__main__":
    print('# Where the Bugs are')




if __name__ == "__main__":
    from bookutils import YouTubeVideo
    # YouTubeVideo("w4u5gCgPlmg")


if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




# ## Mining Change Histories

if __name__ == "__main__":
    print('\n## Mining Change Histories')




from pydriller import RepositoryMining  # https://pydriller.readthedocs.io/

import pickle

REPO = 'https://github.com/uds-se/debuggingbook.git'
# REPO = '..'

class ChangeCounter:
    def __init__(self, repo, filter=None, log=False, **kwargs):
        self.repo = repo
        self.log = log

        if filter is None:
            filter = lambda m: True
        self.filter = filter

        self.changes = {}
        self.messages = {}
        self.sizes = {}
        self.hashes = set()
        
        self.mine(**kwargs)

class ChangeCounter(ChangeCounter):
    def mine(self, **kwargs):
        miner = RepositoryMining(self.repo, **kwargs)

        for commit in miner.traverse_commits():
            for m in commit.modifications:
                m.hash = commit.hash
                m.committer = commit.committer
                m.committer_date = commit.committer_date
                m.msg = commit.msg

                if self.filter(m):
                    self.update_stats(m)

class ChangeCounter(ChangeCounter):
    def update_stats(self, m):
        if not m.new_path:
            return

        node = tuple(m.new_path.split('/'))
        
        if m.hash not in self.hashes:
            self.hashes.add(m.hash)
            self.update_size(node, len(m.source_code) if m.source_code else 0)
            self.update_changes(node, m.msg)
            
        self.update_elems(node, m)

    def update_size(self, node, size):
        self.sizes[node] = size
        
    def update_changes(self, node, msg):
        self.changes.setdefault(node, 0)
        self.messages.setdefault(node, [])
        self.changes[node] += 1
        self.messages[node].append(msg)
        
    def update_elems(self, node, m):
        pass

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    with Timer() as t:
        change_counter = ChangeCounter(REPO)

    t.elapsed_time()


if __name__ == "__main__":
    list(change_counter.changes.keys())[:10]


if __name__ == "__main__":
    change_counter.changes[('Chapters.makefile',)]


if __name__ == "__main__":
    change_counter.messages[('Chapters.makefile',)]


if __name__ == "__main__":
    change_counter.sizes[('Chapters.makefile',)]


# ## Past Changes

if __name__ == "__main__":
    print('\n## Past Changes')




import easyplotly as ep
import plotly.graph_objects as go

import math

class ChangeCounter(ChangeCounter):
    def map_node_sizes(self):
        # Default: use log scale
        return {node: math.log(self.sizes[node]) if self.sizes[node] else 0
             for node in self.sizes}

        # Alternative: use sqrt size
        return {node: math.sqrt(self.sizes[node]) for node in self.sizes}

        # Alternative: use absolute size
        return self.sizes

    def map_node_color(self, node):
        if node and node in self.changes:
            return self.changes[node]
        return None
    
    def map_node_text(self, node):
        if node and node in self.changes:
            return self.changes[node]
        return None
    
    def map_hoverinfo(self):
        return 'label+text'
    
    def map_colorscale(self):
        return 'YlOrRd'

    def map(self):
        treemap = ep.Treemap(
                     self.map_node_sizes(),
                     text=self.map_node_text,
                     hoverinfo=self.map_hoverinfo(),
                     marker_colors=self.map_node_color,
                     marker_colorscale=self.map_colorscale(),
                     root_label=self.repo,
                     branchvalues='total'
                    )

        fig = go.Figure(treemap)
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        
        return fig

if __name__ == "__main__":
    change_counter = ChangeCounter(REPO)


if __name__ == "__main__":
    change_counter.map()


# ## Past Fixes

if __name__ == "__main__":
    print('\n## Past Fixes')




class FixCounter(ChangeCounter):
    def __init__(self, repo, **kwargs):
        super().__init__(repo, filter=self.is_fix, **kwargs)

    def is_fix(self, m):
        return m.msg.startswith("Fix:") and not "show output" in m.msg    

class FixCounter(ChangeCounter):
    def map_node_text(self, node):
        if node and node in self.messages:
            return "<br>".join(self.messages[node])
        return ""
    
    def map_hoverinfo(self):
        return 'label'

if __name__ == "__main__":
    fix_counter = FixCounter(REPO)


if __name__ == "__main__":
    fix_counter.map()


# ## Fine-Grained Changes

if __name__ == "__main__":
    print('\n## Fine-Grained Changes')




# ### Mapping Elements to Locations

if __name__ == "__main__":
    print('\n### Mapping Elements to Locations')




import re

import magic  # https://github.com/ahupp/python-magic

if __name__ == "__main__":
    magic.from_buffer('''
#include <stdio.h>

int main(int argc, char *argv[]) {
    printf("Hello, world!\n")
}
''')


DELIMITERS = [
    (
        # Python
        re.compile(r'^Python.*'),

        # Beginning of element
        re.compile(r'^(async\s+)?(def|class)\s+(?P<name>\w+)\W.*'),

        # End of element
        re.compile(r'^[^#\s]')
    ),
    (
        # Jupyter Notebooks
        re.compile(r'^(JSON|exported SGML|Jupyter).*'),
        re.compile(r'^\s+"(async\s+)?(def|class)\s+(?P<name>\w+)\W'),
        re.compile(r'^(\s+"[^#\s\\]|\s+\])')
    ),
    (
        # C source code
        re.compile(r'^C source.*'),
        re.compile(r'^[^\s].*\s+(?P<name>\w+)\s*[({].*'),
        re.compile(r'^[}]')
    ),
    (
        # Catchall (like C; should work for any language using { } as delimiters)
        re.compile(r'^.*'),
        re.compile(r'^[^\s].*\s+(?P<name>\w+)\s*[({].*'),
        re.compile(r'^[}]')
    )
]

def rxdelim(s):
    tp = magic.from_buffer(s)
    for rxtp, rxbegin, rxend in DELIMITERS:
        if rxtp.match(tp):
            return rxbegin, rxend

    return None, None

def elem_mapping(s, log=False):
    rxbegin, rxend = rxdelim(s)
    if rxbegin is None:
        return []

    mapping = [None]
    current_elem = None
    lineno = 0

    for line in s.split('\n'):
        lineno += 1
        
        match = rxbegin.match(line)
        if match:
            current_elem = match.group('name')
        elif rxend.match(line):
            current_elem = None

        mapping.append(current_elem)
        
        if log:
            print(f"{lineno:3} {current_elem}\t{line}")
        
    return mapping

if __name__ == "__main__":
    some_c_source = """
#include <stdio.h>

int foo(int x) {
    return x;
}

struct bar {
    int x, y;
}

int main(int argc, char *argv[]) {
    return foo(argc);
}

"""
    some_c_mapping = elem_mapping(some_c_source, log=True)


if __name__ == "__main__":
    some_python_source = """
def foo(x):
    return x

class bar(blue):
    x = 25
    def f(x):
        return 26

def main(argc):
    return foo(argc)

"""
    some_python_mapping = elem_mapping(some_python_source, log=True)


# some_jupyter_source = open("Slicer.ipynb").read()
# some_jupyter_mapping = elem_mapping(some_jupyter_source, log=False)

# ### Determining Changed Elements

if __name__ == "__main__":
    print('\n### Determining Changed Elements')




if __package__ is None or __package__ == "":
    from ChangeDebugger import diff, patch, print_patch
else:
    from .ChangeDebugger import diff, patch, print_patch


from diff_match_patch import diff_match_patch

class FineChangeCounter(ChangeCounter):
    def changed_elems(self, mapping, start, length=0):
        elems = set()
        for line in range(start, start + length + 1):
            if line < len(mapping) and mapping[line]:
                elems.add(mapping[line])
                
        return elems

    def elem_size(self, elem, mapping, source):
        source_lines = [''] + source.split('\n')
        size = 0

        for line_no in range(len(mapping)):
            if mapping[line_no] == elem:
                size += len(source_lines[line_no])

        return size

if __name__ == "__main__":
    fine_change_counter = FineChangeCounter(REPO)


if __name__ == "__main__":
    assert fine_change_counter.changed_elems(some_python_mapping, 4) == {'foo'}


if __name__ == "__main__":
    assert fine_change_counter.changed_elems(some_python_mapping, 4, 1) == {'foo', 'bar'}


if __name__ == "__main__":
    assert fine_change_counter.changed_elems(some_python_mapping, 10, 2) == {'main'}


class FineChangeCounter(FineChangeCounter):
    def update_elems(self, node, m):
        old_source = m.source_code_before if m.source_code_before else ""
        new_source = m.source_code if m.source_code else ""
        patches = diff(old_source, new_source)

        old_mapping = elem_mapping(old_source)
        new_mapping = elem_mapping(new_source)

        elems = set()

        for patch in patches:
            old_start_line = patch.start1 + 1
            new_start_line = patch.start2 + 1

            for (op, data) in patch.diffs:
                data_length = data.count('\n')

                if op == diff_match_patch.DIFF_INSERT:
                    elems |= self.changed_elems(old_mapping, old_start_line)
                    elems |= self.changed_elems(new_mapping, new_start_line,
                                                 data_length)
                elif op == diff_match_patch.DIFF_DELETE:
                    elems |= self.changed_elems(old_mapping, old_start_line, 
                                                 data_length)
                    elems |= self.changed_elems(new_mapping, new_start_line)

                old_start_line += data_length
                new_start_line += data_length

        for elem in elems:
            elem_node = node + (elem,)

            self.update_size(elem_node,
                             self.elem_size(elem, new_mapping, new_source))
            self.update_changes(elem_node, m.msg)

if __name__ == "__main__":
    with Timer() as t:
        fine_change_counter = FineChangeCounter(REPO)

    t.elapsed_time()


if __name__ == "__main__":
    fine_change_counter.map()


# ## Synopsis

if __name__ == "__main__":
    print('\n## Synopsis')




if __name__ == "__main__":
    # ignore
    from ClassDiagram import display_class_hierarchy


if __name__ == "__main__":
    # ignore
    display_class_hierarchy([FineChangeCounter, FixCounter],
                            project='debuggingbook')


# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: _Title_

if __name__ == "__main__":
    print('\n### Exercise 1: _Title_')




if __name__ == "__main__":
    # Some code that is part of the exercise
    pass


if __name__ == "__main__":
    # Some code for the solution
    2 + 2


# ### Exercise 2: _Title_

if __name__ == "__main__":
    print('\n### Exercise 2: _Title_')




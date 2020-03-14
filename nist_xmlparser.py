#!/usr/bin/python
XML_FILENAME = './800-53-controls.xml'

import xml.etree.ElementTree as et
import re


class ControlClassNoneException(Exception):
    """
    This class is used for exception handling. This is used for when a variable that
    is supose to hold a control is set to None. An example of its use can be found in
    the print_control_tags method.

    You can create your own exception classes for situations you need.
    There benefit comes in when you are debugging or intending for the situation
    to occur.
    """
    pass

class NIST800:
    """
    The NIST800 Class.
    """
    def __init__(self, xml_filename):
        """
        Initialize NIST800 Class.
        """
        self.tree = et.parse(xml_filename)
        self.root = self.tree.getroot()
        self.parent_map = dict((c, p) for p in self.root.iter() for c in p)
        # This regular expression is used to match namespaces.
        self.regex_ns = re.compile('{..*}')
        self.regex_assignment = re.compile('\[Assignment: organiz(ed|ation)-defined (.*?)\]')

    def __get_control__(self, tag, text):
        """
        Internal function to get a specific control. In Python '__function__' is the notation
        that suggests this functions intended use is internal only, but there is nothing stopping
        you from using it directly. (try it out). Python is an object oriented programming language.
        However, unlike Java and C++, there is nothing that enforces 'private'.
        tag - One of the xml tags used inside the control. Good candidates for this are
              number and title. But try to experiment with it to see what happens when
              you use different tags:
              * Would it return multiple controls if controls share the same tag-text combo?
                (The answer is no, but why?)
        text - Used to identify the control you want.
        """
        root = self.root
        for control in list(root):
            for item in list(control):
                if self.regex_ns.match(item.tag) and item.text == text:
                    return control
        return None

    def generate_assignment_document(self):
        """
        Returns a list of document assignments.
        """
        assignment_document = []
        for item in self.root.iter():
            tag = self.regex_ns.sub('', item.tag)
            if tag == 'title':
                heading = "[{}]\n".format(item.text)
                insert_heading = True
            if tag == 'number':
                number = item.text
            insert_comment = True
            result = self.regex_assignment.findall(item.text)
            if result:
                comment = "#{}: {}\n".format(number, item.text)
                for r in result:
                    if insert_heading:
                        assignment_document.append(heading)
                        insert_heading = False
                    if insert_comment:
                        assignment_document.append(comment)
                        insert_comment = False
                    assignment_document.append("{}\n".format(r[1]))
                assignment_document.append("\n")
        return assignment_document

    def print_assignment_document(self, file_name):
        """
        Create a file and populate it with the assignment document.
        """
        document = self.generate_assignment_document()
        f = open(file_name, 'w')
        for line in document:
            f.write(line)
        f.close()

    def print_control_tags(self, tag, text):
        """
        Print out the control tags with tabs showing hierarchy.
        """
        ctrl = self.__get_control__(tag, text)
        if ctrl == None:
            raise ControlClassNoneException()
        depth = [ctrl]
        for item in ctrl.iter():
            tag = self.regex_ns.sub('', item.tag)
            if tag == 'control':
                continue
            if self.parent_map[item] not in depth:
                depth.append(self.parent_map[item])
            if self.parent_map[item] in depth and \
                    self.parent_map[item] != depth[-1]:
                        idx = len(depth) - (depth.index(self.parent_map[item])+1)
                        depth = depth[:-idx]
            print("\t"*(len(depth)-1) + tag)

    def print_control(self, tag, text):
        """
        Print out a specific control.
        """
        ctrl = self.__get_control__(tag, text)
        for item in ctrl.iter():
            print(item.text, end=" ")
        print()

    def print_all_controls(self):
        """
        Print out all controls.
        """
        for item in self.root.iter():
            print(item.text, end=" ")
        print()

if __name__ == '__main__':
    px = NIST800(XML_FILENAME)
    px.print_control('number', 'AC-1')

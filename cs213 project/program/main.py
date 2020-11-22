import numpy
from collections import Counter
import matplotlib.pyplot as plot
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys
import os


class InterFace:
    def __init__(self):
        self.root = Tk()
        self.filePlace = "input.TXT"
        self.length_of_2dlist = 0
        self.width_of_2dlist = 0
        self.Canvas1 = Canvas(self.root, width=1200, height=800)
        self.Canvas1.pack(pady=10, padx=10)
        self.root.title('reading club app')
        self.root.geometry('1200x800')
        self.root.resizable(False, False)

        # buttons
        self.load_image = PhotoImage(file="6e9yIl.png", master=self.root)
        self.load_image2 = PhotoImage(file="graph_it.png", master=self.root)
        self.load_image3 = PhotoImage(file="open_file.png", master=self.root)
        self.background2 = Label(self.root, image=self.load_image)
        self.background2.place(relwidth=1, relheight=1)

    def openfile(self):
        self.filePlace = filedialog.askopenfilename(parent=self.root, initialdir="/c",
                                                    title='select a text file', filetype=(("txt files", "*.TXT"),
                                                                                          ("all files", "*.*")))
        return self.filePlace

    def to_get_members_data(self, m, m1, m2):
        with open(self.filePlace, 'r') as input1:
            for line in input1:
                if 'Name:' in line:
                    throw_away = line
                    m.append(throw_away[0:0] + throw_away[6:-1])
                    self.length_of_2dlist += 1
                else:
                    continue
                if 'Mobile:' in line:
                    throw_away = line
                    m1.append(throw_away[0:0] + throw_away[8:-1])
                else:
                    continue
                if 'Email:' in line:
                        throw_away = line
                        m2.append(throw_away[0:0] + throw_away[7:-1])
                else:
                    continue
        input1.close()
        return m, m1, m2

    def to_make_members_tuples(self, m, m1, m2):
        member_data_tuples = (self, m, m1, m2)
        return member_data_tuples

    def to_get_books_data(self, pages, titles, category):
        with open(self.filePlace, 'r') as input1:
            for line in input1:
                if 'Number of pages:' in line:
                    throw_away = line
                    pages.append(int(throw_away[0:0] + throw_away[17:-1]))
                    self.width_of_2dlist += 1
                if 'title:' in line:
                    throw_away = line
                    titles.append(throw_away[0:0] + throw_away[7:-1])
                if 'Category:' in line:
                        throw_away = line
                        category.append(throw_away[0:0] + throw_away[10:-1])
        self.width_of_2dlist = self.width_of_2dlist // self.length_of_2dlist
        input1.close()
        return pages, titles, category

    def change_pages_list_to_2d(self, pages_list):
        pages_list2d = numpy.reshape(pages_list, (self.length_of_2dlist, self.width_of_2dlist))
        return pages_list2d

    def change_titles_lists_to_2d(self, titles_list):
        titles_list2d = numpy.reshape(titles_list, (self.length_of_2dlist, self.width_of_2dlist))
        return titles_list2d

    def change_catgory_lists_to_2d(self, category_list):
        catgory_list2d = numpy.reshape(category_list, (self.length_of_2dlist, self.width_of_2dlist))
        return catgory_list2d


class MemberRanking(InterFace):

    def __init__(self, email_list, members_list, category_list, title_list, pages_list, mobile_list):
        super().__init__()
        self.openfile()
        self.members_list, self.mobile_list, self.email_list = self.to_get_members_data(members_list, mobile_list,
                                                                                        email_list)
        self.pages_list, self.title_list, self.category_list = self.to_get_books_data(pages_list, title_list,
                                                                                      category_list)
        self.pages_list = self.change_pages_list_to_2d(pages_list)
        self.new_title_list = None
        self.sum_total = 0
        self.place_totalBooks_member = []
        self.place_totalPages_member = []
        self.title_list2d = self.change_titles_lists_to_2d(self.title_list)
        self.ranking_TotalBooks_member = []
        self.ranking_TotalPages_member = []
        self.category_ranking = 0
        self.sorted_members_pages = []
        self.sorted_members_books = []
        self.members_tuples = self.to_make_members_tuples(self.members_list, self.mobile_list, self.email_list)

    def get_total_pages_group(self):
        self.sum_total=0.0
        for i in range(0, len(self.pages_list)):
            for j in range(0, len(self.pages_list[:][-1])):
                self.sum_total += self.pages_list[i][j]
        return self.sum_total

    def total_books_group(self):
        self.new_title_list = list(dict.fromkeys(self.title_list))
        return len(self.new_title_list)

    def total_books_member(self):
        list_with_nodup = []
        count_list = []
        place = []
        j = 0
        while j in range(0, len(self.title_list2d)):
            new_list = list(dict.fromkeys(self.title_list2d[j]))
            list_with_nodup.append(new_list)
            j+=1
        for j in range(0, len(self.title_list2d)):
            count_list.append(len(list_with_nodup[j]))
        new_list = sorted(count_list)
        self.ranking_TotalBooks_member = new_list[::-1]
        for a in range(0, len(count_list)):
            for b in range(0, len(count_list)):
                if count_list[b] == self.ranking_TotalBooks_member[a]:
                    place.append(b)
        self.place_totalBooks_member = list(dict.fromkeys(place))
        for i in range(0, len(self.place_totalBooks_member)):
            value = self.place_totalBooks_member[i]
            self.sorted_members_books.append(self.members_list[value])
        return self.sorted_members_books, self.ranking_TotalBooks_member

    def get_total_pages_members(self):
        pages1d_total = []
        sum_total = 0.0
        place = []
        for i in range(0, len(self.pages_list)):
            for j in range(0, len(self.pages_list[:][-1])):
                sum_total += self.pages_list[i][j]
            pages1d_total.append(sum_total)
            sum_total = 0.0
        new_list = sorted(pages1d_total)
        self.ranking_TotalPages_member = new_list[::-1]
        for a in range(0, len(pages1d_total)):
            for b in range(0, len(pages1d_total)):
                if pages1d_total[b] == self.ranking_TotalPages_member[a]:
                    place.append(b)
        self.place_totalPages_member = list(dict.fromkeys(place))
        for i in range(0, len(self.place_totalPages_member)):
            value = self.place_totalPages_member[i]
            self.sorted_members_pages.append(self.members_list[value])
        return self.sorted_members_pages, self.ranking_TotalPages_member

    def ranking_categories(self):
        self.category_ranking = Counter()
        for word in self.category_list:
            self.category_ranking[word] += 1
        self.category_ranking = dict(sorted(self.category_ranking.items(), key=lambda x: x[1], reverse=True))
        return self.category_ranking

    def plotting_members_pages(self):
        x_units = []
        y_units = []
        x_units.extend(range(0, len(self.ranking_TotalPages_member)))
        y_units.extend(list(self.ranking_TotalPages_member))
        label = []
        for i in range(0, len(self.place_totalPages_member)):
            label.append(self.sorted_members_pages[i])
        plot.bar(x_units, y_units, tick_label=label, width=0.5)
        plot.xlabel('Names')
        plot.ylabel('pages')
        plot.title('Ranking of group members based on number of pages read')
        plot.show()

    def plotting_members_books(self):
        x_units = []
        y_units = []
        x_units.extend(range(0, len(self.ranking_TotalBooks_member)))
        y_units.extend(list(self.ranking_TotalBooks_member))
        label = []
        for i in range(0, len(self.place_totalBooks_member)):
            label.append(self.sorted_members_books[i])
        plot.bar(x_units, y_units, tick_label=label, width=0.5)
        plot.xlabel('Names')
        plot.ylabel('pages')
        plot.title('Ranking of group members based on number of books read')
        plot.show()

    def plotting_categories(self):
        plot.xlabel('category')
        plot.ylabel('number')
        plot.title('Ranking of categories based on number of readings')
        plot.bar(*zip(*self.category_ranking.items()), width=0.3)
        plot.show()

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def interface2(self):
        button1 = Button(self.background2, image=self.load_image2, border=0, highlightbackground="#37d3ff",
                         command=self.plotting_categories)
        button1.place(relx=0.3, rely=0.5, anchor=CENTER)
        button2 = Button(self.background2, image=self.load_image2, border=0, command=self.plotting_members_books)
        button2.place(relx=0.5, rely=0.5, anchor=CENTER)
        button3 = Button(self.background2, image=self.load_image2, border=0, command=self.plotting_members_pages)
        button3.place(relx=0.7, rely=0.5, anchor=CENTER)
        button4 = Button(self.background2, image=self.load_image3, border=0, command=self.restart_program)
        button4.place(relx=0.5, rely=0.9, anchor=CENTER)

        # tree styling
        style_tree = ttk.Style(self.background2)
        style_tree.configure("Treeview",
                             background="gray",
                             foreground="gray",
                             filedbackground="gray")
        style_tree.map('Treeview', background=[('selected', 'brown')])

        # tree column
        tree1 = ttk.Treeview(self.background2)
        tree2 = ttk.Treeview(self.background2)
        tree3 = ttk.Treeview(self.background2)
        tree2['columns'] = ("members", "books")
        tree3['columns'] = ("members", "pages")
        tree1['columns'] = ("category", "number")

        # format
        tree1.column("#0", width=0, stretch=NO)
        tree1.column("category", anchor=W, width=100, minwidth=10)
        tree1.column("number", anchor=CENTER, width=100, minwidth=10)
        tree2.column("#0", width=0, stretch=NO)
        tree2.column("members", anchor=W, width=140, minwidth=10)
        tree2.column("books", anchor=CENTER, width=60, minwidth=10)
        tree3.column("#0", width=0, stretch=NO)
        tree3.column("members", anchor=W, width=140, minwidth=10)
        tree3.column("pages", anchor=CENTER, width=60, minwidth=10)

        # heading
        tree1.heading("category", text="category", anchor=W)
        tree1.heading("number", text="number", anchor=CENTER)
        tree2.heading("members", text="members", anchor=W)
        tree2.heading("books", text="books", anchor=CENTER)
        tree3.heading("members", text="members", anchor=W)
        tree3.heading("pages", text="pages", anchor=CENTER)

        # adding data
        for row in self.category_ranking:
            tree1.insert("", index='end', values=(row, self.category_ranking[row]))
        for row in range(0, len(self.sorted_members_books)):
            tree2.insert("", index='end', values=(self.sorted_members_books[row], self.ranking_TotalBooks_member[row]))
        tree2.insert("", index='end', values=('Total books by the group', self.total_books_group()))
        for row in range(0, len(self.sorted_members_books)):
            tree3.insert("", index='end', values=(self.sorted_members_pages[row], self.ranking_TotalPages_member[row]))
        tree3.insert("", index='end', values=('Total pages by the group', self.get_total_pages_group()))
        tree1.place(relx=0.3, rely=0.3, anchor=CENTER)
        tree2.place(relx=0.5, rely=0.3, anchor=CENTER)
        tree3.place(relx=0.7, rely=0.3, anchor=CENTER)
        self.root.mainloop()


def main():
    members_list = []
    mobile_list = []
    email_list = []
    pages_list = []
    title_list = []
    category_list = []

    # class calling
    o2 = MemberRanking(email_list, members_list, category_list, title_list, pages_list, mobile_list)
    o2.total_books_member()
    o2.ranking_categories()
    o2.total_books_group()
    o2.get_total_pages_members()

    # interface
    o2.interface2()


if __name__ == '__main__':
    main()

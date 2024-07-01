import xml.dom.minidom
from tkinter import *
from tkinter import colorchooser
from tkinter import filedialog


def setbg():
    color = colorchooser.askcolor()
    if color[1]:
        window.config(bg=color[1])


def uploadxml():
    filepath = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if filepath:  # If the user selected a file (didn't cancel)
        global states
        global transitions
        global initialState
        global finalStates
        global dfa
        global alphabets
        states.clear()
        transitions.clear()
        finalStates.clear()
        alphabets.clear()
        dfa = xml.dom.minidom.parse(filepath)

        # get values in alphabet Tag by its tag and add it to alphabet list in line 7 to 10
        alphabets_xml = dfa.getElementsByTagName('alphabet')
        for alphabet in alphabets_xml:
            alphabets.append(alphabet.getAttribute('letter'))

        # get values in transition Tag by its tag and add it to states list in line 13 to 16
        states_xml = dfa.getElementsByTagName('state')
        for state in states_xml:
            states.append(state.getAttribute('name'))

        # get initialState by its tag
        initial_xml = dfa.getElementsByTagName('initialState')
        initialState = initial_xml[0].getAttribute('name')

        final_xml = dfa.getElementsByTagName('finalState')
        for state in final_xml:
            finalStates.append(state.getAttribute('name'))

        transitions_xml = dfa.getElementsByTagName('transition')
        for transition in transitions_xml:
            source = str(transition.getAttribute('source'))
            destination = str(transition.getAttribute('destination'))
            label = str(transition.getAttribute('label'))
            transitions[(source, label)] = destination
        guid.config(state=NORMAL)
        steps.config(state=NORMAL)
        answer.config(state=NORMAL)
        entry.delete(0, END)
        guid.delete('1.0', END)
        steps.delete('1.0', END)
        answer.delete('1.0', END)
        guid.insert(END,
                    f'Alphabets: {str(alphabets)}\nStates: {str(states)}\nFinal States: {str(finalStates)}\nInitial State: {initialState}\nTransitions:{transitions}')
        guid.config(state=DISABLED)
        steps.config(state=DISABLED)
        answer.config(state=DISABLED)


def symbolCheck(event):  # a definition that checks input string alphabets are in DFA alphabet or not.\
    answer.config(state=NORMAL)
    answer.delete('1.0', 'end-1c')
    steps.config(state=NORMAL)
    ok = True
    for symbol in entry.get():
        if symbol in alphabets:
            ok = True
        else:
            ok = False
            break
    if ok:  # if all alphabets in input string are in DFA Alphabet then check String
        DFACheck()
    else:
        steps.delete('1.0', END)
        steps.insert(END, 'symbol error!')
        steps.config(fg='red')
        answer.insert(END, 'symbol isn\'t in alphabet.')
        answer.config(fg='red', state=DISABLED)
    steps.config(state=DISABLED)


def DFACheck():
    answer.delete('1.0', END)
    steps.delete('1.0', END)
    current_state = initialState
    ok = True
    steps.insert(END, current_state)
    if current_state not in finalStates:
        ok = False
    for symbol in entry.get():
        if (current_state, symbol) in transitions:
            current_state = transitions[(current_state, symbol)]
            steps.insert(END, ' -> ' + current_state)
            ok = True
        else:  # trap State
            fail()
            steps.insert(END, ' -> ' + '∅')
            ok = False
            break
    if ok:
        if current_state in finalStates:
            steps.config(fg='green')
            accept()
        else:
            steps.config(fg='red')
            fail()
    if len(entry.get()) == 0 and ok is not True:
        steps.config(fg='red')
        fail()


def fail():
    answer.config(state=NORMAL)
    answer.insert(END, 'The input string is not accepted.')
    answer.config(fg='red')
    answer.config(state=DISABLED)


def accept():
    answer.config(state=NORMAL)
    answer.insert(END, 'The input string is accepted.')
    answer.config(fg='green')
    answer.config(state=DISABLED)


dfa = xml.dom.minidom.parse('test2.xml')
automata = dfa.documentElement

# get values in alphabet Tag by its tag and add it to alphabet list in line 7 to 10
alphabets_xml = dfa.getElementsByTagName('alphabet')
alphabets = []
for alphabet in alphabets_xml:
    alphabets.append(alphabet.getAttribute('letter'))

# get values in transition Tag by its tag and add it to states list in line 13 to 16
states_xml = dfa.getElementsByTagName('state')
states = []
for state in states_xml:
    states.append(state.getAttribute('name'))

# get initialState by its tag
initial_xml = dfa.getElementsByTagName('initialState')
initialState = initial_xml[0].getAttribute('name')

final_xml = dfa.getElementsByTagName('finalState')
finalStates = []
for state in final_xml:
    finalStates.append(state.getAttribute('name'))

transitions_xml = dfa.getElementsByTagName('transition')
transitions = {

}
for transition in transitions_xml:
    source = str(transition.getAttribute('source'))
    destination = str(transition.getAttribute('destination'))
    label = str(transition.getAttribute('label'))
    transitions[(source, label)] = destination

window = Tk()
window.geometry('500x300')
window.resizable(width=False, height=False)
window.title('DFA(Deterministic Finite Automata)')
window.configure(background='gray')

entry = Entry(window, width=100, fg='black', bg='white')
entry.pack(padx=(10, 10), pady=(10, 25))

answer = Text(window, width=50, height=0)
answer.config(state=DISABLED)
answer.pack()

steps = Text(window, height=5)
steps.pack(padx=10, pady=(10, 10))
steps.config(state=DISABLED)
symbolCheck(event=None)
entry.bind("<KeyRelease>", symbolCheck)

guid = Text(window, height=5, fg='blue', wrap='none')
guid.pack(padx=10, pady=(10, 10))
guid.insert(END,
            f'Alphabets: {str(alphabets)}\nStates: {str(states)}\nFinal States: {str(finalStates)}\nInitial State: {initialState}\nTransitions:{transitions}')
guid.config(state=DISABLED)

menubar = Menu(window)
menubar.add_cascade(label='Upload XML', command=uploadxml)
menubar.add_cascade(label='BackGroundColor', command=setbg)
window.config(menu=menubar)
mainloop()

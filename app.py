from h2o_wave import ui, app, main, data
import pandas as pd
import sys

# This function is to Handling Files: get the csv file which has the dataset.

def fileHandler():
    # The file name is referenced manually
    fileName = './DataSheet1.csv'
    try:
        f = open(fileName, 'r')
    except FileNotFoundError:
        # Throws error if the csv file is not found
        print(f"File {fileName} not found.  Aborting")
        sys.exit(1)
        # Throws error if there is any OS errors
    except OSError:
        print(f"OS error occurred trying to open {fileName}")
        sys.exit(1)
    except Exception as err:
        # Throws error other than the previous errors occur
        print(f"Unexpected error opening {fileName} is", repr(err))
        sys.exit(1)  # or replace this with "raise" ?
    else:
        with f:
            return pd.read_csv(fileName)
        
# This function is to return the data which is fetched from the csv file
# It will return a list of tuples;
# Those tuples have 2 elements; data-> string, price-> float


def contentTaker():
    file = fileHandler()
    file.PassengerId = file.PassengerId.interpolate(
        method='linear',
        limit_direction='forward',
        axis=0
    )
    file.PassengerId = file.PassengerId.fillna(method='bfill')
    listOfData = list(file.itertuples(index=False, name=None))
    return listOfData[:]


# Set variable dataSet
dataSet = contentTaker()

# This function is to convert the all elements in the tuples to string
def stringifyContent(intList):
    return [list(map(str, i)) for i in intList]

# Indicate that a function is a query handler.
@app('/')
# It control the user inputs after the program run.
async def controller(q):
    # Grab a reference to the page at route '/plot'
    if not q.client.intialized:
        mainApp(q)
        table_view(q)
        # footer(q)
  #  elif q.args.table:
   #     table_view(q)
   # elif q.args.plot:
  #      plot_view(q)

    # Finally, save the page.
    await q.page.save()

# This the main app which always show; the program starts,through the all activities


def mainApp(q):
    # insted of using site to give a page name, we use app
    # It is used to control attributes of the active page.
    q.page['activePageController'] = ui.meta_card(
        # make the window responsive, and arrnge the every card
        theme='light',
        box='activePageController',
        layouts=[
            ui.layout(
                # Breakpoints suits to device range
                breakpoint='l',
                zones=[
                    ui.zone('header'),
                    #ui.zone('navigator'),
                    ui.zone('content'),
                    ui.zone('footer'),
                ]),
        ])
    # The header panel
    q.page['header'] = ui.header_card(
        box='header',  # in top left corner with 2 unit height and width
        subtitle="Passengers Details",
        icon='BarChartVerticalFilterSolid',
        title='''Titanic dataset''',
    )
    # The footer frame
    q.page['footer'] = ui.footer_card(
        box='footer',
        caption='''
        © SyThulasi All Rights Reserved.'''
    )
    # This helps to view the Table_View when starting the program
    q.client.intialized = True



# A view for table only.
# Containing all the table related things
def table_view(q):
    # To delete a card named plot_view from a page
    # It helps to view only the plot_view.
    del q.page['plot_view']
    # Stringify the content because ui.table -> rows -> table_row expect only strings
    stringDataSet = stringifyContent(dataSet)
    q.page['table_view'] = ui.form_card(
        box='content',
        items=[
            ui.text_xl(content='Table View'),
            ui.table(
      #  PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Fare,Embarked
                name="data_table",
                columns=[
                    ui.table_column(
                        name='PassengerId', label='Passenger ID', sortable=True, searchable=True),
                    ui.table_column(
                        name='Survived', label='Survived', sortable=True, ),
                    ui.table_column(
                        name='Pclass', label='Class', sortable=True, ),
                    ui.table_column(
                        name='Name', label='Name', sortable=True, searchable=True),
                    ui.table_column(
                        name='Sex', label='Sex', sortable=True, ),
                    ui.table_column(
                        name='Age', label='Age', sortable=True, ),
                    ui.table_column(
                        name='SibSp', label='SibSp', sortable=True, searchable=True),
                    ui.table_column(
                        name='Parch', label='Parch', sortable=True, ),
                    ui.table_column(
                        name='Fare', label='Fare', sortable=True, ),
                    ui.table_column(
                        name='Embarked', label='Embarked', sortable=True, ),
                ],
                rows=[
                    ui.table_row(
                        name=str(1),
                        cells=stringDataSet[i]
                    ) for i in range(len(stringDataSet))
                ],
                downloadable=True,
                height='600px',
                resettable=True,
            ),
        ],
    )



from h2o_wave import Q, ui, app, main

@app('/displayData')

async def server(q: Q):
    
    apply_layout(q)
    show_homepage(q)

    await q.page.save()

def apply_layout(q:Q):
    q.page['meta'] = ui.meta_card(
        box='', 
        theme='nord', 
        layouts=[
            ui.layout(
                breakpoint='xl',
                width='1600px',
                zones=[
                    ui.zone('header'),
                    ui.zone('footer')
                ]
            )
        ]
    )


def show_homepage(q: Q):
    q.page['header'] = ui.header_card(
        box = ui.box('header', 
        width='100%', 
        height='86px'),
        icon='Money',
        icon_color='Black',
        title='Paris Housing Market',
        subtitle='This is an imaginary housing dataset')

    q.page['footer'] = ui.footer_card(
        box='footer', 
        caption='This dataset was obtained from [Kaggle](https://www.kaggle.com/datasets/mssmartypants/paris-housing-price-prediction)')
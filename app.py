from h2o_wave import Q, ui, app, main

@app('/displayData')

async def serve(q: Q):
    q.page['card1'] = ui.form_card(box='1 1 2 2 ', items=[
        ui.text(content = 'Hellow, World'),
    ])
    await q.page.save()
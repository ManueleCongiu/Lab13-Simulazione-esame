import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        SightingsList = self._model.listSightings

        for n in SightingsList:
            if n.datetime.year not in self._listYear:
                self._listYear.append(n.datetime.year)
            if n.shape not in self._listShape and n.shape != "":
                self._listShape.append(n.shape)

        for s in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))
        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        self._view.update_page()

    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value

        self._model.buildGraph(year, shape)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_nodes()} "
                                                      f"Numero di archi: {self._model.get_num_edges()}"))

        for i in self._model.weight_edges():
            self._view.txt_result.controls.append(ft.Text(f"Nodo {i[0]}, somma pesi su archi = {i[1]}"))

        self._view.update_page()

    def handle_path(self, e):
        self._model.searchPath()

        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {str(self._model.solBest)}"))

        for ii in self._model.path_edge:
            self._view.txtOut2.controls.append(ft.Text(f"{ii[0].id} --> {ii[1].id}: weight {ii[2]}"
                                                       f" distance {str(self._model.get_distance_weight(ii))}"))

        self._view.update_page()

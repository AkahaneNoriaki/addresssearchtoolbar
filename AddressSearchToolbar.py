from qgis.PyQt.QtWidgets import QLineEdit, QPushButton, QAction
from qgis.core import QgsExpression, QgsFeatureRequest
print("### AddressSearchToolbar.py LOADED ###")
class AddressSearchToolbar:

    def __init__(self, iface):
        self.iface = iface
        self.toolbar = None
        self.search_edit = None
        self.search_button = None

    def initGui(self):
        self.toolbar = self.iface.addToolBar("Address Search")
        self.toolbar.setObjectName("AddressSearchToolbar")

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("地番を入力")
        self.search_edit.setMinimumWidth(250)
        self.toolbar.addWidget(self.search_edit)

        self.search_button = QPushButton("検索")
        self.search_button.clicked.connect(self.run_search)
        self.toolbar.addWidget(self.search_button)
        
    def unload(self):
        if self.toolbar:
            self.iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar = None
    def run_search(self):
        text = self.search_edit.text().strip()

        if not text:
            self.iface.messageBar().pushWarning(
                "住所検索", "地番を入力してください"
            )
            return

        layer = self.iface.activeLayer()

        if layer is None:
            self.iface.messageBar().pushWarning(
                "住所検索", "アクティブなレイヤがありません"
            )
            return

        # ★ ここで住所フィールド名を指定（仮）
        address_field = "地番"

        if address_field not in [f.name() for f in layer.fields()]:
            self.iface.messageBar().pushCritical(
                "住所検索", f"フィールド「{address_field}」が見つかりません"
            )
            return

        # 検索条件（部分一致・大文字小文字無視）
        expr = QgsExpression(
            f"lower(\"{address_field}\") LIKE lower('%{text}%')"
        )

        request = QgsFeatureRequest(expr)

        ids = [f.id() for f in layer.getFeatures(request)]

        if not ids:
            self.iface.messageBar().pushInfo(
                "住所検索", "該当する地物がありません"
            )
            return

        # 地物を選択
        layer.selectByIds(ids)

        # ズーム
        self.iface.mapCanvas().zoomToSelected(layer)

        self.iface.messageBar().pushSuccess(
            "住所検索", f"{len(ids)} 件ヒットしました"
        )

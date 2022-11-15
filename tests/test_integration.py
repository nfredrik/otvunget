from datetime import datetime
from elspot import main


DATA = f"""
 <!doctype html>
 <html lang="sv-SE">
 <body data-cmplz=1>
 <tbody>
                 <tr class="bg-gray-300 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">{datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                                 <td class="text-right pt-2 pr-2">0,08 öre/kWh</td>
                             </tr>
                     <tr class="bg-gray-200 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">2022-10-11 01:00</td>
                                 <td class="text-right pt-2 pr-2">0,07 öre/kWh</td>
                             </tr>
                     <tr class="bg-gray-300 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">2022-10-11 02:00</td>
                                 <td class="text-right pt-2 pr-2">0,45 öre/kWh</td>                         
                           </tr>
                             </tbody>
 </body>
 </html>
 """

class aMock():
    def __init__(self):
        self.cntr = 0

    def get_data(self) -> str:
        if self.cntr == 0:
            self.cntr+=1
            return DATA

        raise KeyboardInterrupt


def test_main():
    a_mock = aMock()
    rty = main(a_mock)
    assert rty == 1

    # assert that jsonfile and csvfile created!

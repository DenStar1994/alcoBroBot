import sqlite3
import re
class SQLighter:
    # дергаем данные из БД

    #TODO добавить общее подтверждение заказа is_order_confirm
    def get_order_pos(cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select type ||' '|| item ||' '|| cnt||' шт.' from (select at.v_name type, ai.v_name item, sum(o.quantity) cnt from alco_item ai join alco_types at on at.id_alco_types = ai.id_alco_type join orders o on o.id_alco_item = ai.id_alco_item and (o.is_confirm_order = 1 or o.is_confirm_order is null)  and o.is_delivered is null and o.is_confirm = 1 and o.id_user = " + str(cid)+" group by at.v_name, ai.v_name)")
        result = cursor.fetchall()
        conn.close()
        return result

    def total_confirm(is_confirm, cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        print(is_confirm)
        print(cid)
        cursor.execute("update orders set is_confirm_order = " + str(is_confirm) + " where id_user=" + str(
                cid) + " and is_confirm_order is null")
        conn.commit()
        conn.close()

    def get_total_sum(cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "select sum(ai.price*o.quantity) from orders o join alco_item ai on o.id_alco_item = ai.id_alco_item and o.is_delivered is null and o.is_confirm = 1 and o.id_user = "+str(cid)+" group by o.id_user")
        result = cursor.fetchall()
        conn.close()
        return str(result).replace('[(', '').replace(',)]', '') + " руб."

    def get_alco_item(id_alco_type):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select v_name ||' '|| price from alco_item where id_alco_type = " + str(id_alco_type))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_alco_type():
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select v_name from alco_types")
        result = cursor.fetchall()
        conn.close()
        return result

    def get_alco_item_id(v_name):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select id_alco_item from alco_item where v_name = '" + re.sub(r'[^\w\s]+|[\d]+', r'',
                                                                                      v_name).strip() + "'")
        result = cursor.fetchall()
        conn.close()
        return str(result[0])[1:2]

    def get_client_tel(cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select n_tel from clients where id_client = " +str(cid) )
        result = cursor.fetchall()
        conn.close()
        return str(result).replace('[(\'', '').replace('\',)]','')

    def get_client_addr(cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select v_addr from clients where id_client = " +str(cid) )
        result = cursor.fetchall()
        conn.close()
        return str(result).replace('[(\'', '').replace('\',)]','')

    def get_max_id_order():
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select max(id_order) from orders")
        result = cursor.fetchall()
        conn.close()
        return str(result[0])[1:2]

    def if_known_client(cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("select 1 from clients where id_client = "+str(cid))
        result = cursor.fetchall()
        conn.close()
        if str(result) == '[]':
            return 0
        else:
            return 1

    def insert_order(id_order, id_alco_item, cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "insert into orders (dt_insert, id_order, id_alco_item, id_user) values "
            "(datetime('now')," + str(id_order) + "," + str(id_alco_item) + ", " + str(cid) + ") ")
        conn.commit()
        conn.close()

    def update_quantity_order(quantity, cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "update orders set quantity = " + str(quantity) + " where id_user=" + str(cid) + " and quantity is null")
        conn.commit()
        conn.close()

    def confirm_order(is_confirm, cid):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "update orders set is_confirm = " + str(is_confirm) + " where id_user=" + str(
                cid) + " and is_confirm is null")
        conn.commit()
        conn.close()

    def insert_client(id_order, n_tel, cid, v_name):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "insert into clients (dt_insert, id_client, v_name, n_tel, id_order) values "
            "(datetime('now')," + str(cid) + ",'" + str(v_name) + "','" + str(n_tel) + "'," + str(id_order) + ") ")
        conn.commit()
        conn.close()

    def update_client_addr(cid, v_addr):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "update clients set v_addr ='" + str(v_addr) + "' where id_client = " + str(cid))
        conn.commit()
        conn.close()

    def update_client_tel(cid, n_tel):
        conn = sqlite3.connect('AlcoBD.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            "update clients set n_tel ='" + str(n_tel) + "' where id_client = " + str(cid))
        conn.commit()
        conn.close()
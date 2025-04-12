from sqlalchemy import Table, delete, select
from sqlalchemy.orm import Session
from config.db import meta, engine

# Lista de tablas que hacen referencia a facturas
dependent_factura_tables = [
    "pagos",
    "produccion_general_leche",
    "ventas"
]

def eliminarFactura(db: Session, factura_id: int):
    try:
        for table_name in dependent_factura_tables:
            table = Table(table_name, meta, autoload_with=engine)

            # Determina el nombre de la columna relacionada con factura
            if 'factura_id' in table.c:
                stmt = delete(table).where(table.c.factura_id == factura_id)
                db.execute(stmt)

            elif 'id_factura_asociada' in table.c:
                stmt = delete(table).where(table.c.id_factura_asociada == factura_id)
                db.execute(stmt)

        # Finalmente elimina la factura
        factura_table = Table("facturas", meta, autoload_with=engine)
        stmt = delete(factura_table).where(factura_table.c.factura_id == factura_id)
        db.execute(stmt)

        db.commit()
        print(f"✅ Factura {factura_id} eliminada correctamente.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error al eliminar factura {factura_id}: {e}")

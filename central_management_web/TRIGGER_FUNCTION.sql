
class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # Tạo function để cập nhật sĩ số
            """
            CREATE OR REPLACE FUNCTION update_class_size()
            RETURNS TRIGGER AS $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    UPDATE clazz 
                    SET si_so = si_so + 1
                    WHERE class_id = NEW.class_id;
                ELSIF TG_OP = 'DELETE' THEN
                    UPDATE clazz 
                    SET si_so = si_so - 1
                    WHERE class_id = OLD.class_id;
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
            """,
            # Xóa function khi rollback
            """
            DROP FUNCTION IF EXISTS update_class_size();
            """
        ),
        migrations.RunSQL(
            # Tạo trigger cho bảng enrollments
            """
            CREATE TRIGGER update_class_size_trigger
            AFTER INSERT OR DELETE ON enrollments
            FOR EACH ROW
            EXECUTE FUNCTION update_class_size();
            """,
            # Xóa trigger khi rollback
            """
            DROP TRIGGER IF EXISTS update_class_size_trigger ON enrollments;
            """
        ),
    ]
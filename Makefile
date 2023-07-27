requirements:
	@pip freeze > requirements.txt

docker-run:
	@docker compose up --build

docker-clean:
	@docker system prune -a

TABLES := users experiment experimentcompound compound usermetric globalmetric
view-db-records:
	@for table in $(TABLES); do \
		docker exec -it sal_backend-db-1 psql -U postgres -d science -c "SELECT * FROM $$table;"; \
	done

drop-db-tables:
	@for table in $(TABLES); do \
        docker exec -it sal_backend-db-1 psql -U postgres -d science -c "DROP TABLE IF EXISTS $$table CASCADE;"; \
    done

view-db-schema:
	@docker exec -it sal_backend-db-1 psql -U postgres -d science -c "\dt"


trigger-etl:
	@echo "Triggering ETL.."
	@curl http://localhost:5000/etl-trigger
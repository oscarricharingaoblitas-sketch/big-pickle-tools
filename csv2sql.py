import csv, sys, os

def csv_to_sql(csv_path, table_name, batch_size=1000):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        col_list = ', '.join(f'"{c}"' for c in columns)
        
        yield f"CREATE TABLE IF NOT EXISTS {table_name} ({col_list});"
        yield f"INSERT INTO {table_name} ({col_list}) VALUES"
        
        batch = []
        row_count = 0
        for row in reader:
            values = []
            for c in columns:
                v = row[c]
                if v is None or v == '':
                    values.append('NULL')
                else:
                    escaped = v.replace("'", "''")
                    values.append(f"'{escaped}'")
            batch.append(f"({', '.join(values)})")
            row_count += 1
            
            if len(batch) >= batch_size:
                yield ",\n".join(batch) + ";"
                batch = []
                yield f"INSERT INTO {table_name} ({col_list}) VALUES"
        
        if batch:
            yield ",\n".join(batch) + ";"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert CSV to SQL INSERT statements")
    parser.add_argument("csv_file", help="Input CSV file")
    parser.add_argument("--table", "-t", default="data", help="Target table name")
    parser.add_argument("--output", "-o", help="Output SQL file (default: stdout)")
    parser.add_argument("--batch", "-b", type=int, default=1000, help="Batch size")
    args = parser.parse_args()

    lines = list(csv_to_sql(args.csv_file, args.table, args.batch))
    output = "\n".join(lines)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Written {len(lines)} lines to {args.output}")
    else:
        print(output)

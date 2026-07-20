def history_clean_up(history_file_full_path):
    lines = []
    count = 0
    with open(history_file_full_path) as f:
        lines = f.readlines()
        print(lines,len(lines))

history_clean_up('src/functionality_units/update_habit/history/choose_fields_to_update.txt')
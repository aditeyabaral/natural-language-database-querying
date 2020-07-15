python tagDatabase.py || exit 1
echo "Finished iter 1"
sed -i "s/\"tags_framek_frameo_online_filter.csv\"/\"tags_framek_frameo_filter.csv\"/" tagDatabase.py
sed -i "s/\(.*= getOnlineTags.*\)/#\1/" videoLookup.py
sed -i "s/\(.*frame_tags.extend(online_tags)\)/#\1/" videoLookup.py
python tagDatabase.py || exit 1
echo "Finished iter 2"
sed -i "s/\"tags_framek_frameo_filter.csv\"/\"tags_frameo_filter.csv\"/" tagDatabase.py
sed -i "s/\(.*frame_keywords =.*\)/#\1/" videoLookup.py
sed -i "s/\(.*frame_tags.extend(frame_keywords)\)/#\1/" videoLookup.py
python tagDatabase.py || exit 1
echo "Finished iter 3"
cp -f videoLookup.py.bak videoLookup.py
sed -i "s/\(.*getTopKCounter.*\)/#\1/" videoLookup.py
sed -i "s/\"tags_frameo_filter.csv\"/\"tags_framek_frameo_online_nofilter.csv\"/" tagDatabase.py
python tagDatabase.py || exit 1
echo "Finished iter 4"
sed -i "s/\"tags_framek_frameo_online_nofilter.csv\"/\"tags_framek_frameo_nofilter.csv\"/" tagDatabase.py
sed -i "s/\(.*= getOnlineTags.*\)/#\1/" videoLookup.py
sed -i "s/\(.*frame_tags.extend(online_tags)\)/#\1/" videoLookup.py
python tagDatabase.py || exit 1
echo "Finished iter 5"
sed -i "s/\"tags_framek_frameo_nofilter.csv\"/\"tags_frameo_nofilter.csv\"/" tagDatabase.py
sed -i "s/\(.*frame_keywords =.*\)/#\1/" videoLookup.py
sed -i "s/\(.*frame_tags.extend(frame_keywords)\)/#\1/" videoLookup.py
python tagDatabase.py || exit 1
echo "Finished iter 6"

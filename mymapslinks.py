
mymaps = dict()




mymaps['Mandag - Ulige']  = 'https://www.google.com/maps/d/edit?mid=1J9x-AU7mJNjT38D7-ZtjsYor3fVFd0M&usp=sharing'
mymaps['Torsdag - Ulige'] = 'https://www.google.com/maps/d/edit?mid=1WGo3xHxQe3WWtRjntNSBZThaLFkwbkg&usp=sharing'
mymaps['Mandag - Lige']   = 'https://www.google.com/maps/d/edit?mid=1Qb5JMxIHftZCh2_NqvYR0XGS3ac2azk&usp=sharing'
mymaps['Torsdag - Lige']  = 'https://www.google.com/maps/d/edit?mid=19bU0xF1ZJUwMSSjM2A_QwoJgIyPAz90&usp=sharing'



def get_map_url(key):
    return mymaps[key]
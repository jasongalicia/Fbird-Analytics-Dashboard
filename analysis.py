from date import Date
import math

# The analysis class which will help us analyzing and getting us statistics
class Analysis:

    # Intializing the class
    def __init__(self, rows):
        self.rows = rows

    # Returns the list
    def get_list(self):
        return self.rows

    # Returns the list length
    def get_list_length(self):
        return len(self.rows)

    # Returns the average score based on a date
    def get_avg_score(self, date):
        date = str(date)
        if self.get_list_length() == 0:
            return 0.0
        else:
            sum = 0.0
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                if date == str(self.rows[i][3]):
                    sum += self.rows[i][2]
                    count += 1.0
            if count == 0.0:
                return 0.0
            return round(sum / count, 2)

    # Gets the current month average based on a date
    def get_currentmonth_avg(self, date):
        date = str(date)
        if self.get_list_length() == 0:
            return 0.0
        else:
            sum = 0.0
            count = 0.0
            split_date = date.split("-")
            for i in range(0, self.get_list_length(), 1):
                split = str(self.rows[i][3]).split("-")
                if split_date[1] == split[1]:
                    sum += self.rows[i][2]
                    count += 1.0
            if count == 0.0:
                return 0.0
            return round(sum / count, 2)

    # Get's the yearly/annual average based on a date
    def get_yearly_avg(self, date):
        date = str(date)
        if self.get_list_length() == 0:
            return 0.0
        else:
            sum = 0.0
            count = 0.0
            split_date = date.split("-")
            for i in range(0, self.get_list_length(), 1):
                split = str(self.rows[i][3]).split("-")
                if split_date[0] == split[0]:
                    sum += self.rows[i][2]
                    count += 1.0
            if count == 0.0:
                return 0.0
            return round(sum / count, 2)

    # Get's the lifetime average
    def get_lifetime_avg(self):
        if self.get_list_length() == 0:
            return 0.0
        else:
            sum = 0.0
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                sum += self.rows[i][2]
                count += 1.0
            if count == 0.0:
                return 0.0
        return round(sum / count, 2)

    # Standard Deviation based on a date
    def get_sd(self, date):
        sd = self.get_v(date)
        if sd == 0.0:
            return 0.0
        return round(math.sqrt(sd), 2)

    # Variance based on a date
    def get_v(self, date):
        date = str(date)
        if self.get_list_length() == 0:
            return 0.0
        else:
            new_list = []
            sum = 0.0
            for i in range(0, len(self.rows), 1):
                if date == str(self.rows[i][3]):
                    new_list.append(self.rows[i])
                    sum += self.rows[i][2]
            n = len(new_list)
            if n == 0 or n == 1:
                return 0.0
            mean = sum / float(n)
            net_sum = 0.0
            for i in range(0, n, 1):
                net_sum += math.pow(abs((new_list[i][2] - mean)), 2)
            return round(net_sum / (n-1.0), 2)

    # Gets the games played on a certain date
    def get_games_played(self, date):
        date = str(date)
        if self.get_list_length() == 0:
            return 0.0
        else:
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                if date == str(self.rows[i][3]):
                    count += 1.0
            return count

    # Gets the list of scores based on a date
    def get_scores_list(self, date):
        date = str(date)

        if self.get_list_length() == 0:
            list = tuple()
            return list
        else:
            new_list = []
            for i in range(0, self.get_list_length(), 1):
                if date == str(self.rows[i][3]):
                    new_list.append(self.rows[i])
            return new_list

    # Median, assuming the list has already been sorted (ascending)
    def get_lifetime_median(self):
        if self.get_list_length() == 0:
            return 0.0
        elif self.get_list_length() == 1:
            return self.rows[0][2]
        else:
            n = self.get_list_length()
            if n % 2 == 0:
                spot = int(n/2)
                median = (self.rows[spot-1][2] + self.rows[spot][2]) / 2.0
                return round(median, 2)
            else:
                median = self.rows[int(n/2)][2]
                return round(median, 2)

    # Get's the lifetime standard deviation
    def get_lifetime_sd(self):
        sd = math.sqrt(self.get_lifetime_v())
        return round(sd, 2)

    # Get's the lifetime variance
    def get_lifetime_v(self):
        if self.get_list_length() == 0 or self.get_list_length() == 1:
            return 0.0
        else:
            sum = 0.0
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                sum += self.rows[i][2]
                count += 1.0
            mean = sum / count
            print('The mean is: ' + str(mean))
            net_sum = 0.0
            for i in range(0, self.get_list_length(), 1):
                net_sum += math.pow(abs((self.rows[i][2] - mean)), 2)
                print('The net sum is ' + str(net_sum))
            return round((net_sum / (count-1.0)), 2)

    # Gets the percentage of scores above the median
    def get_above_medp(self):
        if self.get_list_length() == 0:
            return 0.0
        else:
            count = 0.0
            median = self.get_lifetime_median()
            for i in range(0, self.get_list_length(), 1):
                if self.rows[i][2] > median:
                    count += 1.0
            percentage = (count / self.get_list_length()) * 100.0
            return round(percentage, 2)

    # Get's the percentage of scores that are equal to the median
    def get_equal_medp(self):
        if self.get_list_length() == 0:
            return 0.0
        else:
            count = 0.0
            median = self.get_lifetime_median()
            for i in range(0, self.get_list_length(), 1):
                if self.rows[i][2] == median:
                    count += 1.0
            percentage = (count / self.get_list_length()) * 100.0
            return round(percentage, 2)

    # Get's date of when a user joined/signed up
    def get_profile_datejoined(self, username):
        for i in range(0, self.get_list_length(), 1):
            if username == str(self.rows[i][1]):
                return str(self.rows[i][3])
        return None

    # Get's the best score based on a specific username
    def get_profile_bestscore(self, username):
        if self.get_list_length() == 0:
            return 0.0
        else:
            list = []
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                if username == str(self.rows[i][1]):
                    list.append(self.rows[i])
                    count += 1.0
            if count == 0.0:
                return 0.0
            else:
                sorter = Sorter()
                new_list = sorter.sort_descending(list)
                return str(new_list[0][2])

    # Gets the average score of all games based on a username
    def get_profile_avgscore(self, username):
        if self.get_list_length() == 0:
            return 0.0
        else:
            list = []
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                if username == str(self.rows[i][1]):
                    count += 1.0
                    list.append(self.rows[i])
            if count == 0.0:
                return 0.0
            else:
                sum = 0.0
                for i in range(0, len(list), 1):
                    sum += list[i][2]
                return round(sum / count, 2)

    # Get's the number of games played ever by a user
    def get_profile_gp(self, username):
        if self.get_list_length() == 0:
            return 0.0
        else:
            count = 0.0
            for i in range(0, self.get_list_length(), 1):
                if username == str(self.rows[i][1]):
                    count += 1.0
            return count

    # Get's a list of games played recently by a specified user
    def get_rec_usergames(self, username):
        if self.get_list_length() == 0:
            list = tuple()
            return list
        else:
            list = []
            for i in range(0, self.get_list_length(), 1):
                if username == str(self.rows[i][1]):
                    list.append(self.rows[i])
            return list

# The sorter class
class Sorter():
    # Sorts a list from biggest values (scores) to smallest
    def sort_descending(self, list):
        new_list = list

        print(len(new_list))
        for i in range(0, len(new_list), 1):
            highest_indx = i
            for j in range(highest_indx+1, len(new_list), 1):
                if new_list[highest_indx][2] < new_list[j][2]:
                    highest_indx = j
            new_list[i], new_list[highest_indx] = new_list[highest_indx], new_list[i]
        return new_list

    # Sorts a list from smallest values (scores) to biggest
    def sort_ascending(self, list):
        new_list = list

        if len(new_list) == 0:
            return new_list
        else:
            for i in range(0, len(new_list), 1):
                lowest_indx = i
                for j in range(lowest_indx+1, len(new_list), 1):
                    if new_list[lowest_indx][2] > new_list[j][2]:
                        lowest_indx = j
                new_list[i], new_list[lowest_indx] = new_list[lowest_indx], new_list[i]
            return new_list

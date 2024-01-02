vsegs = []
hsegs = []
true_vsegs = []
true_hsegs = []
with open("input.txt") as f:
    x = 0
    y = 0
    true_x = 0
    true_y = 0
    for line in f:
        if len(line.strip()) > 0:
            splits = line.strip().split(" ")
            dir = splits[0]
            length = int(splits[1])
            true_length = int(splits[2][2:7], 16)
            true_dir = "RDLU"[int(splits[2][7])]
            match dir:
                case 'U':
                    vsegs.append((x,y-length,y,'U'))
                    y -= length
                case 'D':
                    vsegs.append((x,y,y+length,'D'))
                    y += length
                case 'L':
                    hsegs.append((x-length,x,y))
                    x -= length
                case 'R':
                    hsegs.append((x,x+length,y))
                    x += length
            match true_dir:
                case 'U':
                    true_vsegs.append((true_x,true_y-true_length,true_y,'U'))
                    true_y -= true_length
                case 'D':
                    true_vsegs.append((true_x,true_y,true_y+true_length,'D'))
                    true_y += true_length
                case 'L':
                    true_hsegs.append((true_x-true_length,true_x,true_y))
                    true_x -= true_length
                case 'R':
                    true_hsegs.append((true_x,true_x+true_length,true_y))
                    true_x += true_length

min_y = min([s[1] for s in vsegs])
max_y = max([s[2] for s in vsegs])

right_tips = set([(s[1],s[2]) for s in hsegs])

volume = 0
for y in range(min_y,max_y+1):
    xs = sorted([(s[0],s[3]) for s in vsegs if y >= s[1] and y <= s[2]])
    i = 0
    if xs[0][1] == 'U':
        while i < len(xs):
            start_i = i
            assert xs[i][1] == 'U' # Should always be the case
            i += 1
            if xs[i][1] == 'U': # We're on a hseg, keep going
                i += 1
            while True:
                assert xs[i][1] == 'D' # Should always be the case; impossible to bump into three up segments in a row
                end_i = i
                i += 1
                if i >= len(xs): break # Stop early if needed
                if xs[i][1] == 'U' and (xs[i][0],y) not in right_tips: # We definitely crossed over empty space, so cut it off here
                    break
                elif xs[i][1] == 'U': # This is a right-tip U, which means the line was never interrupted; we're back into filled-in space after this
                    i += 1
                else:
                    assert xs[i][1] == 'D' # Just making sure
                    end_i = i # This is definitely it, two downs in a row means that the space has run out
                    i += 1
                    break
            volume += xs[end_i][0] - xs[start_i][0] + 1
    else:
        while i < len(xs):
            start_i = i
            assert xs[i][1] == 'D' # Should always be the case
            i += 1
            if xs[i][1] == 'D': # We're on a hseg, keep going
                i += 1
            while True:
                assert xs[i][1] == 'U' # Should always be the case; impossible to bump into three up segments in a row
                end_i = i
                i += 1
                if i >= len(xs): break # Stop early if needed
                if xs[i][1] == 'D' and (xs[i][0],y) not in right_tips: # We definitely crossed over empty space, so cut it off here
                    break
                elif xs[i][1] == 'D': # This is a right-tip U, which means the line was never interrupted; we're back into filled-in space after this
                    i += 1
                else:
                    assert xs[i][1] == 'U' # Just making sure
                    end_i = i # This is definitely it, two downs in a row means that the space has run out
                    i += 1
                    break
            volume += xs[end_i][0] - xs[start_i][0] + 1

print(f"The volume of the small lagoon is {volume} cubic meters.")

hsegs = true_hsegs
vsegs = true_vsegs

min_y = min([s[1] for s in vsegs])
max_y = max([s[2] for s in vsegs])

right_tips = set([(s[1],s[2]) for s in hsegs])

volume = 0
percent = 1
for y in range(min_y,max_y+1):
    xs = sorted([(s[0],s[3]) for s in vsegs if y >= s[1] and y <= s[2]])
    i = 0
    if xs[0][1] == 'U':
        while i < len(xs):
            start_i = i
            assert xs[i][1] == 'U' # Should always be the case
            i += 1
            if xs[i][1] == 'U': # We're on a hseg, keep going
                i += 1
            while True:
                assert xs[i][1] == 'D' # Should always be the case; impossible to bump into three up segments in a row
                end_i = i
                i += 1
                if i >= len(xs): break # Stop early if needed
                if xs[i][1] == 'U' and (xs[i][0],y) not in right_tips: # We definitely crossed over empty space, so cut it off here
                    break
                elif xs[i][1] == 'U': # This is a right-tip U, which means the line was never interrupted; we're back into filled-in space after this
                    i += 1
                else:
                    assert xs[i][1] == 'D' # Just making sure
                    end_i = i # This is definitely it, two downs in a row means that the space has run out
                    i += 1
                    break
            volume += xs[end_i][0] - xs[start_i][0] + 1
    else:
        while i < len(xs):
            start_i = i
            assert xs[i][1] == 'D' # Should always be the case
            i += 1
            if xs[i][1] == 'D': # We're on a hseg, keep going
                i += 1
            while True:
                assert xs[i][1] == 'U' # Should always be the case; impossible to bump into three up segments in a row
                end_i = i
                i += 1
                if i >= len(xs): break # Stop early if needed
                if xs[i][1] == 'D' and (xs[i][0],y) not in right_tips: # We definitely crossed over empty space, so cut it off here
                    break
                elif xs[i][1] == 'D': # This is a right-tip U, which means the line was never interrupted; we're back into filled-in space after this
                    i += 1
                else:
                    assert xs[i][1] == 'U' # Just making sure
                    end_i = i # This is definitely it, two downs in a row means that the space has run out
                    i += 1
                    break
            volume += xs[end_i][0] - xs[start_i][0] + 1
    actual_percent = (y - min_y) / (max_y - min_y) * 100
    if actual_percent > percent:
        print(f"{percent}% done...")
        percent += 1

# Note: both of these loops could easily be optimized a bit more, due to the fact that consecutive rows will produce the same volume if no "meaningful" rows are encountered.
# Here a meaningful row could be considered any row that contains the endpoint of a segment, either horizontal or vertical.
# So simply take note where the meaningful rows are, and when an iteration of the loop is finished, multiply its volume output by the number of rows it can skip, and advance the iteration by the same amount of rows.

print(f"The volume of the large lagoon is {volume} cubic meters.")
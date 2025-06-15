#!/usr/bin/env ruby

regex = /hbt{1,}n/

ARGV.each do |arg|
  if arg.match?(regex)
    puts arg
  else
    puts ''
  end
end

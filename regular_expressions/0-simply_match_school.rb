#!/usr/bin/env ruby

regex = /School/

ARGV.each do |arg|
  matches = arg.scan(regex)
  puts matches.join if matches.any?
end

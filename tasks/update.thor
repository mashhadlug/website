#!/usr/bin/env ruby
# encodings: utf-8

require 'thor'
require 'pry'
# require all files in lib
Dir[File.expand_path("../lib/*.rb", __FILE__)].each { |f| require f }


class Update < Thor
  include Thor::Actions

  desc "next_session <date> <session number>", "updates index.md for next session"
  method_option :all, :type => :boolean, :banner => 'compile, commit and push', :aliases => '-a'
  def next_session(date, session)
    renderer = DummyRenderer.new
    renderer.next_session date, session
    File.open(File.expand_path('../../source/index.md', __FILE__), 'w') do |f|
      f.puts renderer.render
    end

    if options[:all]
      thor 'compile'
      thor 'publish'
    end

    puts "Done with pleasure :)"
  end

  desc 'compile', 'compile all html pages from source files'
  def compile
    run 'python2 webtastic.py'
  end

  desc 'publish', 'publish changes to github'
  def publish
    run 'git commit -m "update index for next session" source/index.md'
    run 'git push'

    inside('html') do
      run 'git commit -m "update index for next session" .'
      run 'git push'
    end
  end
end

Update.start(ARGV)

